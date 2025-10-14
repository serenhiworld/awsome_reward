#!/usr/bin/env python3
"""
网站内容更新工具 - 将最新爬虫数据更新到主网站
"""

import os
import json
import re
from datetime import datetime
import shutil

class WebsiteUpdater:
    def __init__(self):
        self.main_html_path = "index.html"
        self.data_dir = "crawler/data"
        self.backup_dir = "backups"
        self.sample_data_dir = "crawler/sample_data"
        self.sample_json = os.path.join(self.sample_data_dir, "enhanced_deals_sample.json")
        self.required_real_deals = 6

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

    def is_real_deal_link(self, url):
        """判断是否为真实可访问的优惠链接"""
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

    def prepare_real_deals(self, deals):
        """筛选真实优惠并限制为固定数量"""
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

        meets_requirement = len(real_deals) >= self.required_real_deals
        return real_deals[:self.required_real_deals], meets_requirement

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

    def generate_deals_html(self, deals, used_sample=False):
        """生成优惠信息的HTML，并返回展示数量与是否满足要求"""
        display_deals, meets_requirement = self.prepare_real_deals(deals)

        if not display_deals:
            return "", 0, meets_requirement

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        header = f"🎁 今日英国优惠精选 - {len(display_deals)} 个真实商家优惠"
        if used_sample:
            header += "（示例数据）"

        update_line = f"🕒 最新更新: {timestamp}"
        if used_sample:
            update_line += " | ⚠️ 暂无实时数据，展示示例优惠"
        else:
            update_line += " | ✅ 提取真实商家链接"

        html = f"""
    <section id="deals" class="daily-deals">
        <div class="container">
            <div class="daily-deals-section">
                <h2>{header}</h2>
                <p class="update-time">{update_line}</p>
                <div class="deals-container">
"""
        
        for deal in display_deals:
            title_zh = deal.get('title_zh', deal.get('title', ''))
            desc_zh = deal.get('description_zh', deal.get('description', ''))

            # 限制描述长度
            if len(desc_zh) > 100:
                desc_zh = desc_zh[:100] + "..."
                
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
        </div>
    </section>
"""
        return html, len(display_deals), meets_requirement

    def update_website(self, deals_html):
        """更新网站内容"""
        if not os.path.exists(self.main_html_path):
            print("❌ 主网站HTML文件不存在")
            return False
            
        # 读取当前网站内容
        with open(self.main_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 移除旧的爬虫内容
        content = re.sub(
            r'<section[^>]*class="daily-deals"[^>]*>.*?</section>',
            '',
            content,
            flags=re.DOTALL
        )

        # 查找插入位置
        match = re.search(r'<section[^>]*id="benefits"[^>]*>', content)
        if not match:
            print("❌ 未找到插入位置标记")
            return False

        insert_pos = match.start()

        # 插入新内容
        new_content = content[:insert_pos] + deals_html + "\n\n" + content[insert_pos:]
        
        # 写入更新后的内容
        with open(self.main_html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        return True

    def update_from_latest_data(self):
        """从最新数据更新网站"""
        print("🔄 开始更新网站内容...")
        
        # 获取最新数据文件
        json_path, html_path = self.get_latest_data_files()
        if not json_path:
            return False

        used_sample = json_path == self.sample_json

        # 加载数据
        deals = self.load_deals_data(json_path)
        if not deals:
            return False
            
        # 备份网站
        if not self.backup_website():
            return False
            
        # 生成HTML
        deals_html, display_count, meets_requirement = self.generate_deals_html(deals, used_sample=used_sample)

        if not deals_html:
            print("❌ 未找到可展示的真实优惠链接")
            return False

        if not meets_requirement and not used_sample:
            print(f"⚠️ 实时数据不足 {self.required_real_deals} 条真实优惠，已仅展示 {display_count} 条")

        # 更新网站
        if self.update_website(deals_html):
            print("✅ 网站更新成功！")
            print(f"📊 已展示 {display_count} 个真实优惠")
            print("🌐 您可以查看更新后的网站效果")
            return True
        else:
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
