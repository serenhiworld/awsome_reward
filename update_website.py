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
        
    def get_latest_data_files(self):
        """获取最新的数据文件"""
        if not os.path.exists(self.data_dir):
            print("❌ 数据目录不存在，请先运行爬虫")
            return None, None
            
        # 获取所有JSON和HTML文件
        json_files = [f for f in os.listdir(self.data_dir) if f.endswith('.json')]
        html_files = [f for f in os.listdir(self.data_dir) if f.endswith('.html')]
        
        if not json_files or not html_files:
            print("❌ 没有找到数据文件，请先运行爬虫")
            return None, None
            
        # 获取最新文件（按修改时间）
        latest_json = max(json_files, key=lambda f: os.path.getmtime(os.path.join(self.data_dir, f)))
        latest_html = max(html_files, key=lambda f: os.path.getmtime(os.path.join(self.data_dir, f)))
        
        json_path = os.path.join(self.data_dir, latest_json)
        html_path = os.path.join(self.data_dir, latest_html)
        
        print(f"📄 最新JSON文件: {latest_json}")
        print(f"📄 最新HTML文件: {latest_html}")
        
        return json_path, html_path

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

    def generate_deals_html(self, deals):
        """生成优惠信息的HTML"""
        if not deals:
            return ""
            
        html = f"""
    <section class="daily-deals">
        <div class="container">
            <div class="daily-deals-section">
                <h2>🎁 今日英国优惠精选</h2>
                <p class="update-time">更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <div class="deals-container">
"""
        
        for deal in deals:
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
        return html

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
            r'<section class="daily-deals">.*?</section>',
            '',
            content,
            flags=re.DOTALL
        )
        
        # 查找插入位置
        insert_marker = '<section id="benefits" class="benefits">'
        if insert_marker not in content:
            print("❌ 未找到插入位置标记")
            return False
            
        # 插入新内容
        new_content = content.replace(
            insert_marker,
            deals_html + '\n\n    ' + insert_marker
        )
        
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
            
        # 加载数据
        deals = self.load_deals_data(json_path)
        if not deals:
            return False
            
        # 备份网站
        if not self.backup_website():
            return False
            
        # 生成HTML
        deals_html = self.generate_deals_html(deals)
        
        # 更新网站
        if self.update_website(deals_html):
            print("✅ 网站更新成功！")
            print(f"📊 已添加 {len(deals)} 个最新优惠")
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
