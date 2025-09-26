import requests
import json
import re
import time
from datetime import datetime
from html.parser import HTMLParser
import logging
import os
from urllib.parse import urljoin, urlparse

# 导入配置
try:
    from enhanced_config import *
except ImportError:
    # 如果没有enhanced_config，使用默认配置
    BASE_URL = "https://www.latestfreestuff.co.uk"
    MAX_DEALS = 10
    REQUEST_DELAY = 2
    ENABLE_TRANSLATION = True

class SimpleTranslator:
    """简单的翻译服务（可替换为其他翻译API）"""
    
    def __init__(self):
        self.cache = {}  # 翻译缓存
        
    def translate_to_chinese(self, text):
        """简单的英译中（这里使用基础词汇替换，实际应用中建议使用专业翻译API）"""
        if not text or text in self.cache:
            return self.cache.get(text, text)
            
        # 基础词汇替换（可扩展）
        translations = {
            'free': '免费',
            'deal': '优惠',
            'offer': '优惠',
            'discount': '折扣',
            'save': '省钱',
            'sale': '促销',
            'voucher': '优惠券',
            'code': '代码',
            'cashback': '返现',
            'student': '学生',
            'new': '新',
            'exclusive': '独家',
            'limited': '限时',
            'today': '今天',
            'now': '现在',
            'get': '获得',
            'buy': '购买',
            'shop': '购物',
            'online': '在线',
            'delivery': '配送',
            'shipping': '运费',
            'click': '点击',
            'here': '这里',
            'link': '链接',
            'visit': '访问',
            'website': '网站',
            'store': '商店',
            'price': '价格',
            'cheap': '便宜',
            'bargain': '便宜货',
            'member': '会员',
            'signup': '注册',
            'register': '注册',
            'account': '账户'
        }
        
        translated = text.lower()
        for en, zh in translations.items():
            translated = translated.replace(en, zh)
            
        # 保持原文的大小写结构
        result = self._preserve_case_structure(text, translated)
        self.cache[text] = result
        return result
        
    def _preserve_case_structure(self, original, translated):
        """保持原文的大小写结构"""
        if not original:
            return translated
        if original.isupper():
            return translated.upper()
        if original.istitle():
            return translated.title()
        return translated

class DealParser(HTMLParser):
    """HTML解析器"""
    
    def __init__(self):
        super().__init__()
        self.deals = []
        self.current_deal = {}
        self.in_deal_container = False
        self.in_title = False
        self.in_description = False
        self.current_tag = None
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        
        # 检测可能的优惠容器
        if tag in ['article', 'div'] and any('deal' in str(v).lower() or 'post' in str(v).lower() 
                                           for v in attrs_dict.values()):
            self.in_deal_container = True
            self.current_deal = {}
            
        # 检测标题
        if tag in ['h1', 'h2', 'h3', 'h4'] and self.in_deal_container:
            self.in_title = True
            
        # 检测描述
        if tag == 'p' and self.in_deal_container:
            self.in_description = True
            
        # 检测链接 - 获取详情页链接
        if tag == 'a' and self.in_deal_container and 'href' in attrs_dict:
            if 'detail_url' not in self.current_deal:
                self.current_deal['detail_url'] = attrs_dict['href']
                
        # 检测图片
        if tag == 'img' and self.in_deal_container:
            if 'src' in attrs_dict:
                self.current_deal['image'] = attrs_dict['src']
            elif 'data-src' in attrs_dict:
                self.current_deal['image'] = attrs_dict['data-src']
                
    def handle_endtag(self, tag):
        if tag in ['article', 'div'] and self.in_deal_container:
            if self.current_deal and 'title' in self.current_deal:
                self.deals.append(self.current_deal.copy())
            self.in_deal_container = False
            self.current_deal = {}
            
        if tag in ['h1', 'h2', 'h3', 'h4']:
            self.in_title = False
            
        if tag == 'p':
            self.in_description = False
            
    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
            
        if self.in_title and self.in_deal_container:
            self.current_deal['title'] = data
            
        if self.in_description and self.in_deal_container:
            if 'description' not in self.current_deal:
                self.current_deal['description'] = data
            else:
                self.current_deal['description'] += ' ' + data

class EnhancedFreeStuffCrawler:
    """增强版优惠爬虫 - 获取真实优惠链接"""
    
    def __init__(self):
        self.base_url = "https://www.latestfreestuff.co.uk"
        self.translator = SimpleTranslator()
        self.session = requests.Session()
        self.setup_logging()
        
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session.headers.update(self.headers)
        
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('enhanced_crawler.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_page_content(self, url):
        """获取页面内容"""
        try:
            self.logger.info(f"正在获取页面: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            self.logger.error(f"获取页面失败 {url}: {e}")
            return None

    def extract_real_deal_url(self, detail_url):
        """从详情页提取真实的优惠链接（非中转页）"""
        try:
            # 如果已经是外部链接，直接返回
            if 'latestfreestuff.co.uk' not in detail_url:
                return detail_url
                
            # 构建完整URL
            if detail_url.startswith('/'):
                full_url = self.base_url + detail_url
            else:
                full_url = detail_url
                
            self.logger.info(f"正在获取详情页以提取真实链接: {full_url}")
            
            # 获取详情页内容
            detail_content = self.get_page_content(full_url)
            if not detail_content:
                return detail_url
                
            # 首先查找 GET FREEBIE 按钮链接
            get_freebie_pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>[^<]*GET\s+FREEBIE[^<]*</a>'
            freebie_matches = re.findall(get_freebie_pattern, detail_content, re.IGNORECASE)
            
            if freebie_matches:
                claim_url = freebie_matches[0]
                self.logger.info(f"找到 GET FREEBIE 按钮链接: {claim_url}")
                
                # 如果是申请页面，需要进一步提取真实链接
                if 'latestfreestuff.co.uk/claim/' in claim_url:
                    real_url = self._extract_from_claim_page(claim_url)
                    if real_url and real_url != claim_url:
                        return real_url
                elif 'latestfreestuff.co.uk' not in claim_url:
                    # 如果GET FREEBIE直接指向外部链接，直接返回
                    return claim_url
                
            # 首先查找claim页面链接 - 这通常包含真实的优惠链接
            claim_links = re.findall(r'href=["\']([^"\']*\/claim\/[^"\']*)["\']', detail_content, re.IGNORECASE)
            if claim_links:
                for claim_link in claim_links:
                    if claim_link.startswith('/'):
                        claim_url = self.base_url + claim_link
                    else:
                        claim_url = claim_link
                    
                    self.logger.info(f"找到申请页面，正在提取真实链接: {claim_url}")
                    claim_content = self.get_page_content(claim_url)
                    
                    if claim_content:
                        # 从申请页面提取外部链接
                        real_link = self._extract_from_claim_page(claim_content)
                        if real_link:
                            return real_link
                
            # 首先查找最常见的优惠按钮链接 - 按优先级排序
            primary_patterns = [
                # 主要的优惠按钮 - 通常包含特定class
                r'<a[^>]+class=["\'][^"\']*(?:deal-btn|offer-btn|get-deal|visit-store|claim-deal|btn-primary)[^"\']*["\'][^>]+href=["\']([^"\']+)["\']',
                # 带有target="_blank"的外部链接 - 最可能是真实链接
                r'<a[^>]+target=["\']_blank["\'][^>]+href=["\']([^"\']+)["\']',
                r'<a[^>]+href=["\']([^"\']+)["\'][^>]+target=["\']_blank["\']',
                # 包含"Get Deal"、"Visit Store"等文本的链接
                r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>[^<]*(?:Get Deal|Visit Store|Claim Deal|Shop Now|Get Offer|Grab Deal)[^<]*</a>',
                # 包含rel="nofollow"的外部链接
                r'<a[^>]+rel=["\']nofollow["\'][^>]+href=["\']([^"\']+)["\']',
                r'<a[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']nofollow["\']',
            ]
            
            # 次要模式 - 更广泛的搜索
            secondary_patterns = [
                # 任何带有常见按钮class的链接
                r'<a[^>]+class=["\'][^"\']*(?:btn|button)[^"\']*["\'][^>]+href=["\']([^"\']+)["\']',
                # 包含deal, offer, go, visit等关键词的链接
                r'href=["\']([^"\']*(?:deal|offer|promo|discount)[^"\']*)["\']',
                r'href=["\']([^"\']*(?:go|visit|redirect)[^"\']*)["\']',
                # 任何外部域名链接（非本站链接）
                r'href=["\'](https?://(?!(?:www\.)?latestfreestuff\.co\.uk)[a-zA-Z0-9][^"\']*?)["\']'
            ]
            
            # 先尝试主要模式
            for i, pattern in enumerate(primary_patterns):
                matches = re.findall(pattern, detail_content, re.IGNORECASE)
                if matches:
                    for match in matches:
                        url = match if isinstance(match, str) else match[0]
                        if self.is_valid_deal_url(url):
                            self.logger.info(f"找到主要优惠链接 (模式{i+1}): {url}")
                            return url
            
            # 再尝试次要模式
            for i, pattern in enumerate(secondary_patterns):
                matches = re.findall(pattern, detail_content, re.IGNORECASE)
                if matches:
                    for match in matches:
                        # 处理正则表达式可能返回的不同格式
                        if isinstance(match, tuple):
                            url = match[0] if match[0] else (match[1] if len(match) > 1 else None)
                        else:
                            url = match
                            
                        if url and self.is_valid_deal_url(url):
                            self.logger.info(f"找到次要优惠链接 (模式{i+3}): {url}")
                            return url
                            
            # 尝试查找JavaScript重定向
            js_patterns = [
                r'window\.location\.href\s*=\s*["\']([^"\']+)["\']',
                r'window\.location\s*=\s*["\']([^"\']+)["\']',
                r'location\.href\s*=\s*["\']([^"\']+)["\']',
                r'document\.location\s*=\s*["\']([^"\']+)["\']',
            ]
            
            for pattern in js_patterns:
                js_matches = re.findall(pattern, detail_content, re.IGNORECASE)
                if js_matches:
                    url = js_matches[0]
                    if self.is_valid_deal_url(url):
                        self.logger.info(f"找到JS重定向链接: {url}")
                        return url
            
            # 最后尝试查找meta refresh重定向
            meta_pattern = r'<meta[^>]+http-equiv=["\']refresh["\'][^>]+content=["\'][^"\']*url=([^"\']+)["\']'
            meta_matches = re.findall(meta_pattern, detail_content, re.IGNORECASE)
            if meta_matches:
                url = meta_matches[0]
                if self.is_valid_deal_url(url):
                    self.logger.info(f"找到meta重定向链接: {url}")
                    return url
            
            # 尝试查找iframe src（有些网站用iframe嵌入外部链接）
            iframe_pattern = r'<iframe[^>]+src=["\']([^"\']+)["\']'
            iframe_matches = re.findall(iframe_pattern, detail_content, re.IGNORECASE)
            if iframe_matches:
                for url in iframe_matches:
                    if self.is_valid_deal_url(url):
                        self.logger.info(f"找到iframe链接: {url}")
                        return url
                        
            self.logger.warning(f"未找到真实外部链接，使用详情页链接: {full_url}")
            return full_url
            
        except Exception as e:
            self.logger.error(f"提取真实链接失败: {e}")
            return detail_url

    def _extract_from_claim_page(self, claim_url):
        """从申请页面提取真实的优惠链接"""
        try:
            self.logger.info(f"正在从申请页面提取真实链接: {claim_url}")
            
            # 获取申请页面内容
            claim_content = self.get_page_content(claim_url)
            if not claim_content:
                return claim_url
                
            # 查找申请页面中的外部链接
            # 优先查找明显的商家网站链接
            external_patterns = [
                # 查找主要的外部域名链接（排除常见的非优惠链接）
                r'href=["\']((https?://(?!(?:www\.)?(?:latestfreestuff\.co\.uk|google\.com|facebook\.com|twitter\.com|instagram\.com|youtube\.com|analytics\.google\.com|fonts\.googleapis\.com))[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[^"\']*?))["\']',
                # 查找包含商家名称的链接模式
                r'href=["\']((https?://[^"\']*(?:shop|store|buy|deal|offer|promo)[^"\']*?))["\']',
            ]
            
            for pattern in external_patterns:
                matches = re.findall(pattern, claim_content, re.IGNORECASE)
                for match in matches:
                    url = match if isinstance(match, str) else match[0]
                    # 进一步过滤无效链接
                    if self._is_valid_merchant_link(url):
                        self.logger.info(f"从申请页面找到真实优惠链接: {url}")
                        return url
                        
            # 如果没找到外部链接，返回申请页面本身
            return claim_url
            
        except Exception as e:
            self.logger.error(f"从申请页面提取链接时出错: {e}")
            return claim_url
    
    def _is_valid_merchant_link(self, url):
        """验证是否是有效的商家链接"""
        if not url or len(url) < 10:
            return False
            
        url_lower = url.lower()
        
        # 排除明显的无效链接
        invalid_patterns = [
            'javascript:', 'mailto:', 'tel:', '#', 'data:',
            'google.com', 'facebook.com', 'twitter.com', 'instagram.com',
            'youtube.com', 'linkedin.com', 'pinterest.com', 'tiktok.com',
            'fonts.googleapis.com', 'analytics.google.com', 'google-analytics.com',
            'googletagmanager.com', 'recaptcha', 'privacy-policy', 'terms-and-conditions',
            '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico'
        ]
        
        for pattern in invalid_patterns:
            if pattern in url_lower:
                return False
                
        # 必须是外部链接
        if 'latestfreestuff.co.uk' in url_lower:
            return False
            
        # 必须是有效的HTTP(S) URL
        if not url_lower.startswith(('http://', 'https://')):
            return False
            
        return True

    def is_valid_deal_url(self, url):
        """验证是否是有效的优惠链接URL"""
        if not url or len(url) < 10:
            return False
        
        url_lower = url.lower()
        
        # 排除无效链接
        invalid_patterns = [
            'javascript:', 'mailto:', 'tel:', '#', 'data:',
            'void(0)', 'about:blank',
            '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.pdf'
        ]
        
        for pattern in invalid_patterns:
            if pattern in url_lower:
                return False
        
        # 排除明显的社交媒体分享链接
        social_share_patterns = [
            'share', 'sharer', 'intent/tweet', 'pin/create',
            'linkedin.com/in/', 'facebook.com/profile'
        ]
        
        for pattern in social_share_patterns:
            if pattern in url_lower:
                return False
                
        # 排除文件下载链接（通常不是优惠链接）
        file_extensions = ['.pdf', '.doc', '.docx', '.zip', '.rar', '.exe', '.dmg']
        for ext in file_extensions:
            if url_lower.endswith(ext):
                return False
        
        # 检查是否是有效的商店/优惠网站域名
        # 常见的英国购物网站和优惠网站域名
        valid_domains = [
            'amazon.co.uk', 'amazon.com', 'ebay.co.uk', 'ebay.com',
            'argos.co.uk', 'currys.co.uk', 'johnlewis.com', 'marksandspencer.com',
            'tesco.com', 'asda.com', 'sainsburys.co.uk', 'morrisons.com',
            'boots.com', 'superdrug.com', 'next.co.uk', 'hm.com',
            'zara.com', 'asos.com', 'boohoo.com', 'prettylittlething.com',
            'topshop.com', 'newlook.com', 'primark.com', 'tkmaxx.com',
            'virginmedia.com', 'octopus.energy', 'bulb.co.uk', 'edf.co.uk',
            'groupon.co.uk', 'wowcher.co.uk', 'vouchercodes.co.uk',
            'hotukdeals.com', 'myvouchercodes.co.uk', 'retailmenot.com',
            'expedia.co.uk', 'booking.com', 'hotels.com', 'lastminute.com',
            'ryanair.com', 'easyjet.com', 'ba.com', 'trainline.com',
            'whitworths.co.uk', 'discoverysample.com'
        ]
        
        # 解析域名
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # 移除 www. 前缀
            if domain.startswith('www.'):
                domain = domain[4:]
                
            # 如果是已知的购物网站，认为是有效的
            for valid_domain in valid_domains:
                if domain == valid_domain or domain.endswith('.' + valid_domain):
                    return True
                    
            # 如果包含常见的优惠相关关键词，也可能是有效的
            deal_keywords = [
                'deal', 'offer', 'discount', 'coupon', 'promo', 'sale',
                'shop', 'store', 'buy', 'checkout', 'cart', 'order',
                'voucher', 'code', 'cashback', 'reward'
            ]
            
            url_for_keywords = url_lower
            for keyword in deal_keywords:
                if keyword in url_for_keywords:
                    return True
                    
        except Exception:
            pass
            
        # 如果URL长度合理且是外部链接，认为可能是有效的
        return len(url) > 15 and 'latestfreestuff.co.uk' not in url_lower

    def parse_deals(self, html_content):
        """解析优惠信息"""
        if not html_content:
            return []
            
        parser = DealParser()
        parser.feed(html_content)
        
        # 清理和验证数据，并获取真实链接
        valid_deals = []
        for i, deal in enumerate(parser.deals[:5]):  # 限制最多5个，避免过多请求
            if self.is_valid_deal(deal):
                self.logger.info(f"处理第 {i+1}/{len(parser.deals[:5])} 个优惠...")
                
                # 获取真实优惠链接
                if 'detail_url' in deal:
                    real_url = self.extract_real_deal_url(deal['detail_url'])
                    deal['url'] = real_url
                    deal['source_url'] = deal['detail_url']  # 保存原始详情页链接
                    
                deal = self.clean_deal_data(deal)
                valid_deals.append(deal)
                
                # 添加延迟避免频繁请求
                time.sleep(2)
                
        return valid_deals

    def is_valid_deal(self, deal):
        """验证优惠信息"""
        if not deal.get('title'):
            return False
        if len(deal['title']) < 5:
            return False
        if not deal.get('detail_url'):
            return False
        return True

    def clean_deal_data(self, deal):
        """清理优惠数据"""
        # 清理标题
        if 'title' in deal:
            deal['title'] = re.sub(r'\s+', ' ', deal['title']).strip()
            
        # 清理描述
        if 'description' in deal:
            deal['description'] = re.sub(r'\s+', ' ', deal['description']).strip()
            deal['description'] = deal['description'][:300]  # 限制长度
            
        # 修复图片URL
        if 'image' in deal and not deal['image'].startswith('http'):
            if deal['image'].startswith('/'):
                deal['image'] = self.base_url + deal['image']
            else:
                deal['image'] = self.base_url + '/' + deal['image']
                
        # 添加日期
        deal['date'] = datetime.now().strftime('%Y-%m-%d')
        
        return deal

    def translate_deals(self, deals):
        """翻译优惠信息"""
        translated_deals = []
        
        for i, deal in enumerate(deals):
            self.logger.info(f"翻译第 {i+1}/{len(deals)} 个优惠...")
            
            translated_deal = deal.copy()
            
            # 翻译标题
            if 'title' in deal:
                translated_deal['title_zh'] = self.translator.translate_to_chinese(deal['title'])
                
            # 翻译描述
            if 'description' in deal:
                translated_deal['description_zh'] = self.translator.translate_to_chinese(deal['description'])
                
            translated_deals.append(translated_deal)
            time.sleep(0.5)  # 避免过于频繁
            
        return translated_deals

    def save_deals(self, deals):
        """保存优惠信息"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存JSON
        os.makedirs('data', exist_ok=True)
        json_file = f"data/enhanced_deals_{timestamp}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(deals, f, ensure_ascii=False, indent=2)
            
        self.logger.info(f"已保存 {len(deals)} 个优惠到 {json_file}")
        
        # 生成HTML
        html_content = self.generate_html(deals)
        html_file = f"data/enhanced_deals_{timestamp}.html"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return json_file, html_file

    def generate_html(self, deals):
        """生成HTML内容"""
        html = f"""
        <section class="daily-deals">
            <div class="container">
                <div class="daily-deals-section">
                    <h2>🎁 今日英国优惠精选（真实链接版）</h2>
                    <p class="update-time">更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <div class="deals-container">
        """
        
        for deal in deals:
            title_zh = deal.get('title_zh', deal.get('title', ''))
            desc_zh = deal.get('description_zh', deal.get('description', ''))
            if len(desc_zh) > 100:
                desc_zh = desc_zh[:100] + "..."
            
            # 显示真实链接域名
            url = deal.get('url', '#')
            domain = urlparse(url).netloc if url.startswith('http') else '未知'
            
            html += f"""
            <div class="deal-item">
                <h3>{title_zh}</h3>
                <p>{desc_zh}</p>
                <div class="deal-meta">
                    <span class="date">📅 {deal.get('date', '')}</span>
                    <span class="source">🔗 {domain}</span>
                    <a href="{url}" target="_blank" class="deal-link">访问优惠</a>
                </div>
            </div>
            """
            
        html += """
                    </div>
                    <div class="deal-note">
                        <p>💡 所有链接已解析为真实优惠地址，点击直接前往商家官网</p>
                    </div>
                </div>
            </div>
        </section>
        """
        
        return html

    def run_crawler(self):
        """运行增强版爬虫"""
        self.logger.info("开始运行增强版爬虫，获取真实优惠链接...")
        
        # 获取页面
        html_content = self.get_page_content(self.base_url)
        if not html_content:
            self.logger.error("无法获取网站内容")
            return []
            
        # 解析优惠
        deals = self.parse_deals(html_content)
        self.logger.info(f"找到 {len(deals)} 个优惠")
        
        if not deals:
            return []
            
        # 翻译
        translated_deals = self.translate_deals(deals)
        
        # 保存
        json_file, html_file = self.save_deals(translated_deals)
        
        self.logger.info(f"增强版爬虫完成！文件: {json_file}, {html_file}")
        return translated_deals

def main():
    """主函数"""
    from urllib.parse import urlparse
    
    crawler = EnhancedFreeStuffCrawler()
    deals = crawler.run_crawler()
    
    if deals:
        print(f"\n✅ 成功爬取 {len(deals)} 个优惠信息（含真实链接）:")
        for i, deal in enumerate(deals, 1):
            title = deal.get('title_zh', deal.get('title', ''))
            url = deal.get('url', '')
            domain = urlparse(url).netloc if url.startswith('http') else '本地链接'
            print(f"{i}. {title}")
            print(f"   🔗 {domain}")
    else:
        print("❌ 未获取到优惠信息")

if __name__ == "__main__":
    main()
