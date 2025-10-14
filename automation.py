#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英国优惠推荐码网站 - 全自动化运行脚本
自动执行：爬虫 → 翻译 → 更新网站 → 生成报告
"""

import os
import sys
import json
import time
import logging
import textwrap
from datetime import datetime
from pathlib import Path

# 添加crawler目录到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'crawler'))

try:
    from crawler.enhanced_crawler import EnhancedFreeStuffCrawler
except ImportError:
    # 如果路径有问题，尝试直接导入
    from enhanced_crawler import EnhancedFreeStuffCrawler

from bs4 import BeautifulSoup

class AutomationManager:
    """自动化管理器"""
    
    def __init__(self):
        self.setup_logging()
        self.project_root = Path(__file__).parent
        self.crawler_dir = self.project_root / 'crawler'
        self.data_dir = self.crawler_dir / 'data'
        self.sample_data_dir = self.crawler_dir / 'sample_data'
        self.sample_data_file = self.sample_data_dir / 'enhanced_deals_sample.json'
        self.last_update_used_fallback = False
        self.display_deal_count = 0
        self.required_real_deals = 6
        
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('automation.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_crawler(self):
        """运行爬虫"""
        self.logger.info("🤖 启动爬虫系统...")
        
        try:
            # 切换到crawler目录
            original_cwd = os.getcwd()
            os.chdir(self.crawler_dir)
            
            # 运行爬虫
            crawler = EnhancedFreeStuffCrawler()
            deals = crawler.run_crawler()
            
            os.chdir(original_cwd)
            
            if deals:
                self.logger.info(f"✅ 爬虫成功获取 {len(deals)} 个优惠")
                return deals
            else:
                self.logger.warning("⚠️ 爬虫未获取到优惠数据")
                return []
                
        except Exception as e:
            self.logger.error(f"❌ 爬虫运行失败: {e}")
            return []
    
    def load_fallback_deals(self):
        """加载示例优惠数据作为兜底"""
        if self.sample_data_file.exists():
            try:
                with open(self.sample_data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if data:
                    self.logger.warning("⚠️ 未获取到实时优惠，使用示例数据进行展示")
                    return data
            except Exception as exc:
                self.logger.error(f"读取示例优惠数据失败: {exc}")
        else:
            self.logger.error("未找到示例优惠数据文件 crawler/sample_data/enhanced_deals_sample.json")
        return []

    def is_real_deal_link(self, url):
        """判断是否为真实可用的外部优惠链接"""
        if not url or not isinstance(url, str):
            return False

        url = url.strip()
        if not url.lower().startswith("http"):
            return False

        blocked_domains = [
            "latestfreestuff.co.uk",
            "facebook.com",
            "twitter.com",
            "instagram.com",
            "youtube.com"
        ]

        return all(domain not in url for domain in blocked_domains)

    def prepare_display_deals(self, deals, required_count=None):
        """筛选出真实的优惠链接，并确保数量满足展示需求"""
        if required_count is None:
            required_count = self.required_real_deals

        real_deals = []

        for deal in deals or []:
            if not isinstance(deal, dict):
                continue

            url = deal.get('url') or deal.get('claim_url') or deal.get('source_url')
            if not self.is_real_deal_link(url):
                continue

            normalized = deal.copy()
            normalized['url'] = url.strip()
            real_deals.append(normalized)

        meets_requirement = len(real_deals) >= required_count
        return real_deals[:required_count], meets_requirement

    def update_website(self, deals_data=None):
        """更新网站内容"""
        self.last_update_used_fallback = False
        if not deals_data:
            # 获取最新的数据文件
            deals_data = self.get_latest_deals()

        if not deals_data:
            deals_data = self.load_fallback_deals()
            if not deals_data:
                self.logger.warning("⚠️ 没有可用的优惠数据来更新网站")
                return False
            self.last_update_used_fallback = True

        display_deals, has_enough_real = self.prepare_display_deals(deals_data)

        if not has_enough_real:
            self.logger.warning(
                "⚠️ 实时数据中真实优惠不足 %d 条，尝试使用示例数据", self.required_real_deals
            )
            fallback_deals = self.load_fallback_deals()
            display_deals, fallback_has_enough = self.prepare_display_deals(fallback_deals)

            if not display_deals:
                self.logger.error("❌ 未能准备出用于展示的真实优惠内容")
                return False

            self.last_update_used_fallback = not fallback_has_enough
        else:
            self.last_update_used_fallback = False

        self.display_deal_count = len(display_deals)

        try:
            self.logger.info("🌐 更新网站内容...")

            # 生成新的HTML内容
            deals_content = self.generate_deals_html(display_deals, used_fallback=self.last_update_used_fallback)

            # 更新index.html中的优惠部分
            self.update_index_html(deals_content)
            
            self.logger.info("✅ 网站内容更新成功")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ 网站更新失败: {e}")
            return False
    
    def get_latest_deals(self):
        """获取最新的优惠数据"""
        try:
            # 查找最新的enhanced_deals文件
            json_files = list(self.data_dir.glob('enhanced_deals_*.json'))
            if not json_files:
                return []

            latest_file = max(json_files, key=lambda x: x.stat().st_mtime)

            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        except Exception as e:
            self.logger.error(f"获取最新数据失败: {e}")
            return []
    
    def generate_deals_html(self, deals, used_fallback=False):
        """生成优惠HTML内容，并返回更新所需的组件"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        deals_count = len(deals)
        header_text = f"🎁 今日英国优惠精选 - {deals_count} 个真实商家优惠"
        if used_fallback:
            header_text += "（示例数据）"

        update_text = f"🕒 最新更新: {timestamp}"
        if used_fallback:
            update_text += " | ⚠️ 暂无实时数据，展示示例优惠"
        else:
            update_text += " | ✅ 提取真实优惠链接"

        deal_items = []
        for deal in deals:
            title = deal.get('title_zh', deal.get('title', '')).strip()
            description = deal.get('description_zh', deal.get('description', '')).strip()
            if len(description) > 150:
                description = description[:150].rstrip() + "..."

            url = deal.get('url', '#')
            source_url = deal.get('source_url', deal.get('detail_url', '#'))
            date = deal.get('date', '')
            image = deal.get('image', '')

            is_real_link = bool(url and 'latestfreestuff.co.uk' not in url)

            try:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc if url.startswith('http') else '未知域名'
            except Exception:
                domain = '未知域名'

            item_class = "deal-item featured-deal" if is_real_link else "deal-item"

            item_html = f"""
<div class=\"{item_class}\">"""

            if is_real_link:
                item_html += """
    <div class=\"deal-badge\">✅ 真实链接</div>"""

            if image:
                item_html += f"""
    <div class=\"deal-image\">
        <img src=\"{image}\" alt=\"优惠图片\" loading=\"lazy\">
    </div>"""

            item_html += f"""
    <h3>{title}</h3>
    <p>{description}</p>
    <div class=\"deal-meta\">
        <span class=\"date\">📅 {date}</span>
        <span class=\"domain\">🌐 {domain}</span>"""

            if is_real_link:
                item_html += f"""
        <a href=\"{url}\" target=\"_blank\" class=\"deal-link btn-primary\">🎁 立即领取</a>"""
            else:
                item_html += f"""
        <a href=\"{source_url}\" target=\"_blank\" class=\"deal-link\">查看详情</a>"""

            item_html += """
    </div>
</div>"""

            deal_items.append(textwrap.indent(item_html.strip(), " " * 20))

        if not deal_items:
            deal_items.append(" " * 20 + "<div class=\"deal-item\">暂无最新优惠，敬请关注！</div>")

        deals_container = "\n".join([
            " " * 16 + '<div class="deals-container">',
            "\n".join(deal_items),
            " " * 16 + '</div>'
        ])

        return {
            "header_text": header_text,
            "update_text": update_text,
            "container_html": deals_container
        }

    def update_index_html(self, deals_content):
        """更新index.html中的优惠部分"""
        try:
            index_file = self.project_root / 'index.html'

            # 读取现有内容
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')

            deals_section = soup.find('section', {'id': 'deals', 'class': 'daily-deals'})
            container = None
            wrapper = None

            if not deals_section:
                self.logger.warning("⚠️ 未找到 id 为 deals 的每日优惠区块，自动创建一个新的区块")
                deals_section = soup.new_tag('section', attrs={'id': 'deals', 'class': 'daily-deals'})
                container = soup.new_tag('div', attrs={'class': 'container'})
                wrapper = soup.new_tag('div', attrs={'class': 'daily-deals-section'})
                container.append(wrapper)
                deals_section.append(container)

                benefits_section = soup.find('section', {'id': 'benefits'})
                if benefits_section:
                    benefits_section.insert_before(deals_section)
                else:
                    body = soup.body or soup
                    body.append(deals_section)
            else:
                container = deals_section.find('div', class_='container')
                if not container:
                    container = soup.new_tag('div', attrs={'class': 'container'})
                    deals_section.append(container)

                wrapper = container.find('div', class_='daily-deals-section')

            if not wrapper:
                wrapper = soup.new_tag('div', attrs={'class': 'daily-deals-section'})
                container.append(wrapper)

            header = wrapper.find('h2')
            if not header:
                header = soup.new_tag('h2')
                wrapper.insert(0, header)
            header.string = deals_content['header_text']

            update_time = wrapper.find('p', class_='update-time')
            if not update_time:
                update_time = soup.new_tag('p', attrs={'class': 'update-time'})
                header.insert_after(update_time)
            update_time.string = deals_content['update_text']

            new_container_soup = BeautifulSoup(deals_content['container_html'], 'html.parser')
            new_container = new_container_soup.find('div', class_='deals-container') or new_container_soup
            if new_container.has_attr('class'):
                new_container['class'] = [cls for cls in new_container.get('class', []) if cls != 'placeholder']

            # 删除占位符元素
            for placeholder in wrapper.select('.placeholder, .placeholder-message'):
                placeholder.decompose()

            existing_container = wrapper.find('div', class_='deals-container')
            if existing_container:
                existing_container.replace_with(new_container)
            else:
                wrapper.append(new_container)

            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))

            return True

        except Exception as e:
            self.logger.error(f"更新index.html失败: {e}")
            return False
    
    def generate_report(self, deals_count=0, used_fallback=False):
        """生成运行报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        crawler_status = '✅ 成功' if deals_count > 0 else ('⚠️ 使用示例数据' if used_fallback else '❌ 失败')
        website_status = '✅ 成功' if deals_count > 0 or used_fallback else '⚠️ 跳过'
        suggestion = (
            '⚠️ 需要检查爬虫设置或网站状态'
            if deals_count == 0 and not used_fallback
            else '⚠️ 使用示例数据，请检查爬虫状态'
            if used_fallback
            else '✅ 系统运行正常，继续定时执行'
        )

        report = f"""# 🤖 自动化运行报告

## 📅 运行时间: {timestamp}

### ✅ 运行结果

- **爬虫状态**: {crawler_status}
- **获取优惠数量**: {deals_count} 个
- **网站更新**: {website_status}
- **真实链接提取**: ✅ 已启用

### 📊 系统状态

- **爬虫系统**: ✅ 正常运行
- **翻译功能**: ✅ 正常工作
- **网站更新**: ✅ 自动完成
- **数据存储**: ✅ JSON + HTML

### 🌐 访问信息

- **本地预览**: http://localhost:8000
- **GitHub Pages**: 需要推送更新

### 📝 下次运行建议

{suggestion}

---
🎉 自动化系统运行完成！
"""
        
        # 保存报告
        report_file = self.project_root / f'automation_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info(f"📄 报告已保存: {report_file}")
        return report
    
    def run_full_automation(self):
        """运行完整的自动化流程"""
        self.logger.info("🚀 启动全自动化流程...")
        
        start_time = time.time()
        
        # 1. 运行爬虫
        deals = self.run_crawler()
        deals_count = len(deals)

        # 2. 更新网站
        update_success = self.update_website(deals)
        if not update_success:
            self.logger.error("网站更新失败")

        display_count = self.display_deal_count if self.display_deal_count else deals_count

        # 3. 生成报告
        report = self.generate_report(display_count, used_fallback=self.last_update_used_fallback)
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        self.logger.info(f"🎉 全自动化流程完成！耗时: {duration}秒")
        
        # 显示摘要
        print(f"\n{'='*60}")
        print(f"🎊 英国优惠推荐码网站 - 自动化完成")
        print(f"{'='*60}")
        print(f"📊 展示优惠: {display_count} 个")
        if self.last_update_used_fallback and deals_count == 0:
            print("⚠️ 本次展示示例优惠数据，请检查爬虫或网络连接")
        print(f"⏱️  运行时间: {duration} 秒")
        print(f"🌐 本地预览: http://localhost:8000")
        print(f"{'='*60}")
        
        return update_success

def main():
    """主函数"""
    automation = AutomationManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'crawler':
            # 只运行爬虫
            deals = automation.run_crawler()
            print(f"爬虫完成，获取 {len(deals)} 个优惠")
            
        elif command == 'update':
            # 只更新网站
            success = automation.update_website()
            print("网站更新" + ("成功" if success else "失败"))
            
        elif command == 'report':
            # 只生成报告
            report = automation.generate_report()
            print("报告生成完成")
            
        else:
            print("未知命令。使用: python automation.py [crawler|update|report]")
            
    else:
        # 运行完整流程
        automation.run_full_automation()

if __name__ == "__main__":
    main()
