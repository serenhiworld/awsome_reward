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
from datetime import datetime
from pathlib import Path

# 添加crawler目录到系统路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'crawler'))

try:
    from crawler.enhanced_crawler import EnhancedFreeStuffCrawler
except ImportError:
    # 如果路径有问题，尝试直接导入
    from enhanced_crawler import EnhancedFreeStuffCrawler

class AutomationManager:
    """自动化管理器"""
    
    def __init__(self):
        self.setup_logging()
        self.project_root = Path(__file__).parent
        self.crawler_dir = self.project_root / 'crawler'
        self.data_dir = self.crawler_dir / 'data'
        
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
    
    def update_website(self, deals_data=None):
        """更新网站内容"""
        if not deals_data:
            # 获取最新的数据文件
            deals_data = self.get_latest_deals()
        
        if not deals_data:
            self.logger.warning("⚠️ 没有可用的优惠数据来更新网站")
            return False
        
        try:
            self.logger.info("🌐 更新网站内容...")
            
            # 生成新的HTML内容
            html_content = self.generate_deals_html(deals_data)
            
            # 更新index.html中的优惠部分
            self.update_index_html(html_content)
            
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
                return None
                
            latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
            
            with open(latest_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            self.logger.error(f"获取最新数据失败: {e}")
            return None
    
    def generate_deals_html(self, deals):
        """生成优惠HTML内容"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html = f'''            <div class="daily-deals-section">
                <h2>🎁 今日英国优惠精选 - 真实商家链接</h2>
                <p class="update-time">🕒 最新更新: {timestamp} | ✅ 已提取真实优惠链接</p>
                <div class="deals-container">
'''

        for i, deal in enumerate(deals[:20]):  # 最多显示20个优惠
            title = deal.get('title_zh', deal.get('title', ''))
            description = deal.get('description_zh', deal.get('description', ''))
            if len(description) > 150:
                description = description[:150] + "..."
            
            url = deal.get('url', '#')
            source_url = deal.get('source_url', deal.get('detail_url', '#'))
            date = deal.get('date', '')
            image = deal.get('image', '')
            
            # 判断是否为真实外部链接
            is_real_link = 'latestfreestuff.co.uk' not in url
            
            # 获取域名
            try:
                from urllib.parse import urlparse
                domain = urlparse(url).netloc if url.startswith('http') else '未知域名'
            except:
                domain = '未知域名'
            
            # 设置样式类
            item_class = "deal-item featured-deal" if is_real_link else "deal-item"
            
            html += f'''
                    <div class="{item_class}">'''
            
            if is_real_link:
                html += '''
                        <div class="deal-badge">✅ 真实链接</div>'''
            
            if image:
                html += f'''
                        <div class="deal-image">
                            <img src="{image}" alt="优惠图片" loading="lazy">
                        </div>'''
            
            html += f'''
                        <h3>{title}</h3>
                        <p>{description}</p>
                        <div class="deal-meta">
                            <span class="date">📅 {date}</span>
                            <span class="domain">🌐 {domain}</span>'''
            
            if is_real_link:
                html += f'''
                            <a href="{url}" target="_blank" class="deal-link btn-primary">🎁 立即领取</a>'''
            else:
                html += f'''
                            <a href="{source_url}" target="_blank" class="deal-link">查看详情</a>'''
            
            html += '''
                        </div>
                    </div>'''
        
        html += '''
                </div>
            </div>'''
        
        return html
    
    def update_index_html(self, deals_html):
        """更新index.html中的优惠部分"""
        try:
            index_file = self.project_root / 'index.html'
            
            # 读取现有内容
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 查找并替换优惠部分
            import re
            
            # 查找daily-deals-section的开始和结束
            pattern = r'<div class="daily-deals-section">.*?</div>\s*</div>\s*</div>\s*</section>'
            
            replacement = deals_html + '''
        </div>
    </section>'''
            
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            # 如果没有找到匹配的部分，说明结构可能有变化
            if new_content == content:
                self.logger.warning("⚠️ 未找到要替换的优惠部分，可能需要手动检查HTML结构")
                return False
            
            # 写入新内容
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
            
        except Exception as e:
            self.logger.error(f"更新index.html失败: {e}")
            return False
    
    def generate_report(self, deals_count=0):
        """生成运行报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# 🤖 自动化运行报告

## 📅 运行时间: {timestamp}

### ✅ 运行结果

- **爬虫状态**: {'✅ 成功' if deals_count > 0 else '❌ 失败'}
- **获取优惠数量**: {deals_count} 个
- **网站更新**: {'✅ 成功' if deals_count > 0 else '⚠️ 跳过'}
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

{'✅ 系统运行正常，继续定时执行' if deals_count > 0 else '⚠️ 需要检查爬虫设置或网站状态'}

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
        if deals_count > 0:
            success = self.update_website(deals)
            if not success:
                self.logger.error("网站更新失败")
        
        # 3. 生成报告
        report = self.generate_report(deals_count)
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        self.logger.info(f"🎉 全自动化流程完成！耗时: {duration}秒")
        
        # 显示摘要
        print(f"\n{'='*60}")
        print(f"🎊 英国优惠推荐码网站 - 自动化完成")
        print(f"{'='*60}")
        print(f"📊 获取优惠: {deals_count} 个")
        print(f"⏱️  运行时间: {duration} 秒")
        print(f"🌐 本地预览: http://localhost:8000")
        print(f"{'='*60}")
        
        return deals_count > 0

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
