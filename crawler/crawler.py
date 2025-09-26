import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
from googletrans import Translator
import re
import os
from fake_useragent import UserAgent
import logging

class LatestFreeStuffCrawler:
    def __init__(self):
        self.base_url = "https://www.latestfreestuff.co.uk"
        self.ua = UserAgent()
        self.translator = Translator()
        self.session = requests.Session()
        self.setup_logging()
        
        # 设置请求头
        self.headers = {
            'User-Agent': self.ua.random,
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
                logging.FileHandler('crawler.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_page_content(self, url):
        """获取页面内容"""
        try:
            # 添加随机延迟避免被封
            time.sleep(2)
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except Exception as e:
            self.logger.error(f"获取页面失败 {url}: {e}")
            return None

    def parse_deals(self, html_content):
        """解析优惠信息"""
        if not html_content:
            return []
            
        soup = BeautifulSoup(html_content, 'lxml')
        deals = []
        
        # 寻找文章或优惠信息的容器
        # 这里需要根据实际网站结构调整选择器
        deal_containers = soup.find_all('article') or soup.find_all('div', class_=re.compile(r'deal|post|item'))
        
        for container in deal_containers[:10]:  # 限制最多10个优惠
            try:
                deal = self.extract_deal_info(container)
                if deal and self.is_valid_deal(deal):
                    deals.append(deal)
            except Exception as e:
                self.logger.error(f"解析优惠信息失败: {e}")
                continue
                
        return deals

    def extract_deal_info(self, container):
        """从容器中提取优惠信息"""
        deal = {}
        
        # 提取标题
        title_elem = (container.find('h1') or 
                     container.find('h2') or 
                     container.find('h3') or
                     container.find('a'))
        if title_elem:
            deal['title'] = title_elem.get_text().strip()
        else:
            return None
            
        # 提取描述
        desc_elem = (container.find('p') or 
                    container.find('div', class_=re.compile(r'content|desc|summary')))
        if desc_elem:
            deal['description'] = desc_elem.get_text().strip()[:500]  # 限制长度
        else:
            deal['description'] = ""
            
        # 提取链接
        link_elem = container.find('a')
        if link_elem:
            href = link_elem.get('href')
            if href:
                if href.startswith('/'):
                    deal['url'] = self.base_url + href
                elif not href.startswith('http'):
                    deal['url'] = self.base_url + '/' + href
                else:
                    deal['url'] = href
                    
        # 提取图片
        img_elem = container.find('img')
        if img_elem:
            src = img_elem.get('src') or img_elem.get('data-src')
            if src:
                if src.startswith('/'):
                    deal['image'] = self.base_url + src
                elif not src.startswith('http'):
                    deal['image'] = self.base_url + '/' + src
                else:
                    deal['image'] = src
                    
        # 提取日期
        date_elem = container.find('time') or container.find(attrs={'class': re.compile(r'date|time')})
        if date_elem:
            deal['date'] = date_elem.get_text().strip()
        else:
            deal['date'] = datetime.now().strftime('%Y-%m-%d')
            
        return deal

    def is_valid_deal(self, deal):
        """验证优惠信息是否有效"""
        if not deal.get('title'):
            return False
        if len(deal['title']) < 10:  # 标题太短
            return False
        if not deal.get('url'):
            return False
        return True

    def translate_text(self, text, max_retries=3):
        """翻译文本到中文"""
        if not text:
            return ""
            
        for attempt in range(max_retries):
            try:
                # 限制文本长度，避免翻译API限制
                if len(text) > 1000:
                    text = text[:1000] + "..."
                    
                result = self.translator.translate(text, dest='zh-cn')
                return result.text
            except Exception as e:
                self.logger.warning(f"翻译失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    return text  # 翻译失败返回原文

    def translate_deal(self, deal):
        """翻译优惠信息"""
        translated_deal = deal.copy()
        
        # 翻译标题
        translated_deal['title_zh'] = self.translate_text(deal['title'])
        
        # 翻译描述
        if deal.get('description'):
            translated_deal['description_zh'] = self.translate_text(deal['description'])
        
        return translated_deal

    def save_deals_to_json(self, deals, filename=None):
        """保存优惠信息到JSON文件"""
        if not filename:
            filename = f"deals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        filepath = os.path.join('data', filename)
        os.makedirs('data', exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(deals, f, ensure_ascii=False, indent=2)
            
        self.logger.info(f"已保存 {len(deals)} 个优惠信息到 {filepath}")
        return filepath

    def generate_html_content(self, deals):
        """生成HTML内容用于网站展示"""
        html_template = """
        <div class="deals-container">
            <h2>🎁 今日英国优惠精选</h2>
            <p class="update-time">更新时间: {update_time}</p>
            <div class="deals-grid">
                {deals_html}
            </div>
        </div>
        """
        
        deal_template = """
        <div class="deal-card">
            {image_html}
            <div class="deal-content">
                <h3>{title}</h3>
                <p class="deal-description">{description}</p>
                <div class="deal-meta">
                    <span class="deal-date">📅 {date}</span>
                    <a href="{url}" target="_blank" class="deal-link">查看详情 →</a>
                </div>
            </div>
        </div>
        """
        
        deals_html = ""
        for deal in deals:
            image_html = ""
            if deal.get('image'):
                image_html = f'<img src="{deal["image"]}" alt="{deal["title_zh"]}" class="deal-image">'
                
            deal_html = deal_template.format(
                image_html=image_html,
                title=deal.get('title_zh', deal.get('title', '')),
                description=deal.get('description_zh', deal.get('description', ''))[:200] + "...",
                date=deal.get('date', ''),
                url=deal.get('url', '#')
            )
            deals_html += deal_html
            
        final_html = html_template.format(
            update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            deals_html=deals_html
        )
        
        return final_html

    def crawl_and_translate(self):
        """主爬虫流程"""
        self.logger.info("开始爬取最新优惠信息...")
        
        # 获取主页内容
        html_content = self.get_page_content(self.base_url)
        if not html_content:
            self.logger.error("无法获取网站内容")
            return []
            
        # 解析优惠信息
        deals = self.parse_deals(html_content)
        self.logger.info(f"找到 {len(deals)} 个优惠信息")
        
        if not deals:
            return []
            
        # 翻译优惠信息
        translated_deals = []
        for i, deal in enumerate(deals):
            self.logger.info(f"翻译第 {i+1}/{len(deals)} 个优惠...")
            translated_deal = self.translate_deal(deal)
            translated_deals.append(translated_deal)
            time.sleep(1)  # 避免翻译API限制
            
        # 保存数据
        json_file = self.save_deals_to_json(translated_deals)
        
        # 生成HTML内容
        html_content = self.generate_html_content(translated_deals)
        
        # 保存HTML文件
        html_file = os.path.join('data', f"deals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        self.logger.info(f"爬虫完成！生成文件: {json_file}, {html_file}")
        return translated_deals

def main():
    """主函数"""
    crawler = LatestFreeStuffCrawler()
    deals = crawler.crawl_and_translate()
    
    if deals:
        print(f"成功爬取并翻译了 {len(deals)} 个优惠信息")
    else:
        print("未找到优惠信息")

if __name__ == "__main__":
    main()
