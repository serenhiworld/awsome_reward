#!/usr/bin/env python3
"""
简单的演示爬虫 - 用于展示功能
"""

import json
from datetime import datetime
import os

def create_demo_deals():
    """创建演示优惠数据"""
    demo_deals = [
        {
            "title": "Free McDonald's Breakfast",
            "title_zh": "麦当劳免费早餐",
            "description": "Get a free breakfast meal with any hot drink purchase",
            "description_zh": "购买任意热饮即可获得免费早餐",
            "url": "https://example.com/mcdonalds-free-breakfast",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "image": "https://via.placeholder.com/300x200?text=McDonald%27s"
        },
        {
            "title": "ASOS Student Discount 20% Off",
            "title_zh": "ASOS学生优惠20%折扣",
            "description": "Students can get 20% off all full-price items at ASOS",
            "description_zh": "学生可享受ASOS全价商品20%折扣",
            "url": "https://example.com/asos-student-discount",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "image": "https://via.placeholder.com/300x200?text=ASOS"
        },
        {
            "title": "Free Spotify Premium Trial 3 Months",
            "title_zh": "Spotify高级版免费试用3个月",
            "description": "New users can enjoy 3 months of Spotify Premium for free",
            "description_zh": "新用户可免费享受3个月Spotify高级版服务",
            "url": "https://example.com/spotify-free-trial",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "image": "https://via.placeholder.com/300x200?text=Spotify"
        },
        {
            "title": "Tesco Clubcard Double Points Weekend",
            "title_zh": "Tesco会员卡双倍积分周末",
            "description": "Earn double Clubcard points on all purchases this weekend",
            "description_zh": "本周末所有购物可获得双倍会员卡积分",
            "url": "https://example.com/tesco-double-points",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "image": "https://via.placeholder.com/300x200?text=Tesco"
        },
        {
            "title": "Amazon Prime Student - 6 Months Free",
            "title_zh": "亚马逊Prime学生版 - 6个月免费",
            "description": "UK students get 6 months of Amazon Prime absolutely free",
            "description_zh": "英国学生可获得6个月完全免费的亚马逊Prime服务",
            "url": "https://example.com/amazon-prime-student",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "image": "https://via.placeholder.com/300x200?text=Amazon+Prime"
        }
    ]
    
    return demo_deals

def generate_demo_html(deals):
    """生成演示HTML内容"""
    html = f"""
    <section class="daily-deals">
        <div class="container">
            <div class="daily-deals-section">
                <h2>🎁 今日英国优惠精选</h2>
                <p class="update-time">更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (演示数据)</p>
                <div class="deals-container">
    """
    
    for deal in deals:
        html += f"""
                    <div class="deal-item">
                        <h3>{deal['title_zh']}</h3>
                        <p>{deal['description_zh']}</p>
                        <div class="deal-meta">
                            <span class="date">📅 {deal['date']}</span>
                            <a href="{deal['url']}" target="_blank" class="deal-link">查看详情</a>
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

def save_demo_data():
    """保存演示数据"""
    deals = create_demo_deals()
    
    # 创建数据目录
    os.makedirs('data', exist_ok=True)
    
    # 保存JSON
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_file = f"data/demo_deals_{timestamp}.json"
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(deals, f, ensure_ascii=False, indent=2)
    
    # 生成HTML
    html_content = generate_demo_html(deals)
    html_file = f"data/demo_deals_{timestamp}.html"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 演示数据已生成:")
    print(f"   JSON文件: {json_file}")
    print(f"   HTML文件: {html_file}")
    
    return deals, json_file, html_file

def update_demo_website(html_file):
    """更新网站内容（演示版）"""
    try:
        # 读取生成的HTML内容
        with open(html_file, 'r', encoding='utf-8') as f:
            deals_html = f.read()
        
        # 读取主网站文件
        main_html_path = "../index.html"
        if not os.path.exists(main_html_path):
            print("❌ 主网站HTML文件不存在")
            return False
        
        with open(main_html_path, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        # 备份原文件
        backup_path = f"../demo_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(main_content)
        
        # 查找插入位置
        insert_marker = '<section id="benefits" class="benefits">'
        if insert_marker in main_content:
            # 移除旧的演示内容
            import re
            main_content = re.sub(
                r'<section class="daily-deals">.*?</section>',
                '',
                main_content,
                flags=re.DOTALL
            )
            
            # 插入新内容
            new_content = main_content.replace(
                insert_marker,
                deals_html + '\\n\\n    ' + insert_marker
            )
            
            # 写入更新后的内容
            with open(main_html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 演示内容已更新到网站，备份文件: {backup_path}")
            return True
        else:
            print("❌ 未找到插入位置")
            return False
            
    except Exception as e:
        print(f"❌ 更新网站失败: {e}")
        return False

def main():
    print("🚀 英国优惠爬虫演示")
    print("=" * 40)
    
    print("📊 生成演示优惠数据...")
    deals, json_file, html_file = save_demo_data()
    
    print(f"\\n📋 生成了 {len(deals)} 个演示优惠:")
    for i, deal in enumerate(deals, 1):
        print(f"   {i}. {deal['title_zh']}")
    
    print(f"\\n🔄 更新网站内容...")
    if update_demo_website(html_file):
        print("\\n🎉 演示完成！")
        print("💡 现在您可以打开网站查看效果:")
        print("   http://localhost:8000")
        print("\\n📝 要运行真实爬虫，请使用:")
        print("   python3 simple_crawler.py")
    else:
        print("\\n❌ 演示失败，请检查文件结构")

if __name__ == "__main__":
    main()
