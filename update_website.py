#!/usr/bin/env python3
"""
网站内容更新工具 - 将最新爬虫数据更新到主网站
"""

import os
import json
import shutil
from datetime import datetime

from deal_renderer import (
    REQUIRED_REAL_DEALS,
    render_deals_section,
    replace_deals_section,
    select_real_deals,
)

class WebsiteUpdater:
    def __init__(self):
        self.main_html_path = "index.html"
        self.data_dir = "crawler/data"
        self.backup_dir = "backups"
        self.sample_data_dir = "crawler/sample_data"
        self.sample_json = os.path.join(self.sample_data_dir, "enhanced_deals_sample.json")
        self.required_real_deals = REQUIRED_REAL_DEALS

    def get_latest_data_files(self):
        """获取最新的数据文件"""
        if not os.path.exists(self.data_dir):
            print("⚠️ 数据目录不存在，尝试使用示例数据")
            return self.get_sample_data_files()

        # 获取所有JSON和HTML文件
        json_files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
        html_files = [f for f in os.listdir(self.data_dir) if f.endswith('.html')]

        if not json_files:
            print("⚠️ 没有找到JSON数据文件，尝试使用示例数据")
            return self.get_sample_data_files()

        # 获取最新JSON文件（按修改时间）
        latest_json = max(json_files, key=lambda f: os.path.getmtime(os.path.join(self.data_dir, f)))
        json_path = os.path.join(self.data_dir, latest_json)

        latest_html = None
        if html_files:
            latest_html = max(html_files, key=lambda f: os.path.getmtime(os.path.join(self.data_dir, f)))
            html_path = os.path.join(self.data_dir, latest_html)
        else:
            html_path = None

        print(f"📄 最新JSON文件: {latest_json}")
        if latest_html:
            print(f"📄 最新HTML文件: {latest_html}")

        return json_path, html_path

    def get_sample_data_files(self):
        """获取示例数据文件"""
        if os.path.exists(self.sample_json):
            print("⚠️ 使用示例优惠数据进行更新")
            return self.sample_json, None

        print("❌ 未找到示例数据文件，请先运行爬虫生成数据")
        return None, None

    def load_deals_data(self, json_path):
        """加载优惠数据"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                deals = json.load(f)
            print(f"✅ 成功加载 {len(deals)} 个优惠信息")
            return deals
        except Exception as e:
            print(f"❌ 加载数据失败: {e}")
            return []

    def build_deals_section(self, deals):
        """筛选真实优惠并生成用于插入的HTML片段"""
        selected_deals, meets_requirement, total_real = select_real_deals(
            deals,
            required_count=self.required_real_deals,
        )

        if not meets_requirement or not selected_deals:
            return "", len(selected_deals), total_real, False, {}

        section_html, metadata = render_deals_section(selected_deals)
        return section_html, len(selected_deals), total_real, True, metadata

    def backup_website(self):
        """备份当前网站"""
        if not os.path.exists(self.main_html_path):
            print("❌ 主网站文件不存在")
            return False
            
        # 创建备份目录
        os.makedirs(self.backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(self.backup_dir, f"index_backup_{timestamp}.html")
        
        shutil.copy2(self.main_html_path, backup_path)
        print(f"💾 网站已备份到: {backup_path}")
        return True

    def update_website(self, deals_section_html):
        """将生成的优惠区块写入主站HTML"""
        if not os.path.exists(self.main_html_path):
            print("❌ 主网站HTML文件不存在")
            return False

        with open(self.main_html_path, 'r', encoding='utf-8') as f:
            original_html = f.read()

        updated_html, action = replace_deals_section(original_html, deals_section_html)

        with open(self.main_html_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)

        print(
            "✅ 网站内容已更新" if action == 'replaced' else
            "✅ 已插入每日优惠区块" if action == 'inserted' else
            "✅ 已追加每日优惠区块"
        )
        return True

    def update_from_latest_data(self):
        """从最新数据更新网站"""
        print("🔄 开始更新网站内容...")
        
        # 获取最新数据文件
        json_path, html_path = self.get_latest_data_files()
        if not json_path:
            return False

        used_sample = json_path == self.sample_json

        source_text = os.path.relpath(json_path)
        print(f"📦 使用数据源: {source_text}")
        if html_path:
            print(f"🧩 对应HTML片段: {os.path.relpath(html_path)}")

        # 加载数据
        deals = self.load_deals_data(json_path)
        if not deals:
            return False

        # 备份网站
        if not self.backup_website():
            return False

        # 生成HTML片段
        deals_html, display_count, total_real, meets_requirement, metadata = self.build_deals_section(deals)

        if not meets_requirement:
            print(
                f"❌ 实时数据仅 {total_real} 条真实优惠，未达到 "
                f"{self.required_real_deals} 条展示要求"
            )
            return False

        if not deals_html:
            print("❌ 未生成每日优惠区块")
            return False

        if used_sample:
            print("⚠️ 当前使用示例数据，仅用于样式预览")

        if self.update_website(deals_html):
            print("✅ 网站更新成功！")
            print(f"📊 已展示 {display_count} 个真实优惠")
            if metadata:
                print(metadata.get('update_text', ''))
            print("🌐 您可以查看更新后的网站效果")
            return True

        print("❌ 网站更新失败")
        return False

def main():
    print("🔄 网站内容更新工具")
    print("=" * 40)
    
    updater = WebsiteUpdater()
    
    if updater.update_from_latest_data():
        print("\n🎉 更新完成！")
        print("💡 建议操作:")
        print("1. 在浏览器中查看网站效果")
        print("2. 如果满意，可以推送到GitHub: git add . && git commit -m 'Update: Latest deals' && git push")
    else:
        print("\n❌ 更新失败，请检查错误信息")

if __name__ == "__main__":
    main()
