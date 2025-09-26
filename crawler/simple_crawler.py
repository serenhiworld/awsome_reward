import requests
import json
import re
import time
from datetime import datetime
from html.parser import HTMLParser
import logging
import os

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
            'shipping': '运费'
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
            
        # 检测链接
        if tag == 'a' and self.in_deal_container and 'href' in attrs_dict:
            if 'url' not in self.current_deal:
                self.current_deal['url'] = attrs_dict['href']
                
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

class SimpleFreeStuffCrawler:
    """简化版优惠爬虫"""
    
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
                logging.FileHandler('simple_crawler.log', encoding='utf-8'),
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

    def parse_deals(self, html_content):
        """解析优惠信息"""
        if not html_content:
            return []
            
        parser = DealParser()
        parser.feed(html_content)
        
        # 清理和验证数据
        valid_deals = []
        for deal in parser.deals[:10]:  # 限制最多10个
            if self.is_valid_deal(deal):
                deal = self.clean_deal_data(deal)
                valid_deals.append(deal)
                
        return valid_deals

    def is_valid_deal(self, deal):
        """验证优惠信息"""
        if not deal.get('title'):
            return False
        if len(deal['title']) < 5:
            return False
        return True

    def clean_deal_data(self, deal):
        """清理优惠数据"""
        # 清理标题
        if 'title' in deal:
            deal['title'] = re.sub(r'\\s+', ' ', deal['title']).strip()
            
        # 清理描述
        if 'description' in deal:
            deal['description'] = re.sub(r'\\s+', ' ', deal['description']).strip()
            deal['description'] = deal['description'][:300]  # 限制长度
            
        # 修复URL
        if 'url' in deal and not deal['url'].startswith('http'):
            if deal['url'].startswith('/'):
                deal['url'] = self.base_url + deal['url']
            else:
                deal['url'] = self.base_url + '/' + deal['url']
                
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
        json_file = f"data/deals_{timestamp}.json"
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(deals, f, ensure_ascii=False, indent=2)
            
        self.logger.info(f"已保存 {len(deals)} 个优惠到 {json_file}")
        
        # 生成HTML
        html_content = self.generate_html(deals)
        html_file = f"data/deals_{timestamp}.html"
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return json_file, html_file

    def generate_html(self, deals):
        """生成HTML内容"""
        html = """
        <div class="daily-deals-section">
            <h2>🎁 今日英国优惠精选</h2>
            <p class="update-time">更新时间: {}</p>
            <div class="deals-container">
        """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        for deal in deals:
            title_zh = deal.get('title_zh', deal.get('title', ''))
            desc_zh = deal.get('description_zh', deal.get('description', ''))[:100] + "..."
            
            html += f"""
            <div class="deal-item">
                <h3>{title_zh}</h3>
                <p>{desc_zh}</p>
                <div class="deal-meta">
                    <span class="date">📅 {deal.get('date', '')}</span>
                    <a href="{deal.get('url', '#')}" target="_blank" class="deal-link">查看详情</a>
                </div>
            </div>
            """
            
        html += """
            </div>
        </div>
        """
        
        return html

    def run_crawler(self):
        """运行爬虫"""
        self.logger.info("开始爬取优惠信息...")
        
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
        
        self.logger.info(f"爬虫完成！文件: {json_file}, {html_file}")
        return translated_deals

def main():
    """主函数"""
    crawler = SimpleFreeStuffCrawler()
    deals = crawler.run_crawler()
    
    if deals:
        print(f"\\n✅ 成功爬取 {len(deals)} 个优惠信息:")
        for i, deal in enumerate(deals, 1):
            print(f"{i}. {deal.get('title_zh', deal.get('title', ''))}")
    else:
        print("❌ 未获取到优惠信息")

if __name__ == "__main__":
    main()
