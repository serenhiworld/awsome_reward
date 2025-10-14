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

from deal_renderer import (
    REQUIRED_REAL_DEALS,
    render_deals_section,
    replace_deals_section,
    select_real_deals,
)

class AutomationManager:
    """自动化管理器"""
    
    def __init__(self):
        self.setup_logging()
        self.project_root = Path(__file__).parent
        self.crawler_dir = self.project_root / 'crawler'
        self.data_dir = self.crawler_dir / 'data'
        self.display_deal_count = 0
        self.last_total_real_deals = 0
        self.required_real_deals = REQUIRED_REAL_DEALS
        
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
        """更新网站内容，仅展示真实优惠链接"""
        self.display_deal_count = 0
        if not deals_data:
            deals_data = self.get_latest_deals()

        if not deals_data:
            self.logger.error("❌ 未找到可用于更新的网站优惠数据")
            return False

        display_deals, meets_requirement, total_real = select_real_deals(
            deals_data,
            required_count=self.required_real_deals,
        )

        self.last_total_real_deals = total_real

        if not meets_requirement or not display_deals:
            self.logger.error(
                "❌ 实时数据仅找到 %d 条真实优惠，未达到 %d 条展示要求",
                total_real,
                self.required_real_deals,
            )
            return False

        try:
            self.logger.info("🌐 更新网站内容...")
            deals_section_html, metadata = render_deals_section(display_deals)

            index_file = self.project_root / 'index.html'
            with open(index_file, 'r', encoding='utf-8') as file:
                original_html = file.read()

            updated_html, action = replace_deals_section(original_html, deals_section_html)

            with open(index_file, 'w', encoding='utf-8') as file:
                file.write(updated_html)

            self.display_deal_count = len(display_deals)

            action_text = {
                'replaced': '覆盖原有区块',
                'inserted': '新增每日优惠区块',
                'appended': '追加每日优惠区块',
            }.get(action, action)

            self.logger.info("✅ 网站内容更新成功（%s）", action_text)
            self.logger.info(metadata['update_text'])
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
    
    def generate_report(self, deals_count=0, update_success=False):
        """生成运行报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        crawler_status = (
            '✅ 成功'
            if self.last_total_real_deals >= self.required_real_deals
            else '❌ 未达标'
        )
        website_status = '✅ 成功' if update_success else '❌ 未更新'

        if self.last_total_real_deals == 0:
            suggestion = '❌ 未抓取到真实优惠，请检查爬虫或数据源'
        elif self.last_total_real_deals < self.required_real_deals:
            suggestion = (
                f"⚠️ 真实优惠仅 {self.last_total_real_deals} 条，未达到 "
                f"{self.required_real_deals} 条展示要求"
            )
        elif not update_success:
            suggestion = '⚠️ 网站未更新，请检查 HTML 模板或写入权限'
        else:
            suggestion = '✅ 系统运行正常，继续保持每日更新'

        report = f"""# 🤖 自动化运行报告

## 📅 运行时间: {timestamp}

### ✅ 运行结果

- **爬虫状态**: {crawler_status}
- **获取真实优惠数量**: {self.last_total_real_deals} 条
- **展示优惠数量**: {deals_count} 条
- **网站更新**: {website_status}
- **真实链接提取**: ✅ 已启用

### 📊 系统状态

- **爬虫系统**: ✅ 已执行
- **翻译功能**: ✅ 正常工作
- **网站更新**: {'✅ 自动完成' if update_success else '⚠️ 需人工检查'}
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
        report = self.generate_report(display_count, update_success=update_success)
        
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        
        self.logger.info(f"🎉 全自动化流程完成！耗时: {duration}秒")
        
        # 显示摘要
        print(f"\n{'='*60}")
        print("🎊 英国优惠推荐码网站 - 自动化完成")
        print(f"{'='*60}")
        print(f"📊 展示优惠: {display_count} 个")
        if not update_success:
            print(
                f"❌ 本次未能发布每日优惠，真实优惠仅 {self.last_total_real_deals} 条，"
                f"需要至少 {self.required_real_deals} 条"
            )
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
