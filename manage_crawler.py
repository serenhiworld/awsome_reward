#!/usr/bin/env python3
"""
英国优惠爬虫管理工具
支持立即运行、定时调度、网站更新等功能
"""

import os
import sys
import json
import subprocess
import schedule
import time
from datetime import datetime
import argparse

def run_simple_crawler():
    """运行简单爬虫"""
    try:
        result = subprocess.run([sys.executable, 'simple_crawler.py'], 
                              capture_output=True, text=True, cwd='crawler')
        if result.returncode == 0:
            print("✅ 爬虫运行成功")
            print(result.stdout)
        else:
            print("❌ 爬虫运行失败")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 运行爬虫时出错: {e}")
        return False

def update_website():
    """更新网站内容"""
    try:
        # 查找最新的HTML文件
        data_dir = "crawler/data"
        if not os.path.exists(data_dir):
            print("❌ 数据目录不存在")
            return False
            
        html_files = [f for f in os.listdir(data_dir) if f.endswith('.html')]
        if not html_files:
            print("❌ 没有找到HTML文件")
            return False
            
        # 获取最新文件
        latest_html = max(html_files, key=lambda f: os.path.getctime(os.path.join(data_dir, f)))
        html_path = os.path.join(data_dir, latest_html)
        
        # 读取内容
        with open(html_path, 'r', encoding='utf-8') as f:
            deals_html = f.read()
            
        # 读取主网站文件
        main_html_path = "index.html"
        if not os.path.exists(main_html_path):
            print("❌ 主网站HTML文件不存在")
            return False
            
        with open(main_html_path, 'r', encoding='utf-8') as f:
            main_content = f.read()
            
        # 备份原文件
        backup_path = f"index_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(main_content)
            
        # 查找插入位置并插入内容
        insert_marker = '<section id="benefits" class="benefits">'
        if insert_marker in main_content:
            # 移除旧的爬虫内容
            import re
            main_content = re.sub(
                r'<div class="daily-deals-section">.*?</div>\\s*</div>',
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
                
            print(f"✅ 网站更新成功，备份文件: {backup_path}")
            return True
        else:
            print("❌ 未找到插入位置")
            return False
            
    except Exception as e:
        print(f"❌ 更新网站时出错: {e}")
        return False

def scheduled_task():
    """定时任务"""
    print(f"\\n🕒 定时任务开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行爬虫
    if run_simple_crawler():
        # 更新网站
        update_website()
        print("✅ 定时任务完成")
    else:
        print("❌ 定时任务失败")

def start_scheduler():
    """启动定时调度器"""
    print("⏰ 启动定时调度器...")
    
    # 设置定时任务
    schedule.every().day.at("09:00").do(scheduled_task)  # 上午9点
    schedule.every().day.at("18:00").do(scheduled_task)  # 下午6点
    schedule.every().day.at("23:00").do(scheduled_task)  # 晚上11点
    
    # 立即运行一次
    print("🔄 立即运行一次...")
    scheduled_task()
    
    print("⏰ 定时调度器已启动，等待定时任务...")
    print("📅 调度时间: 09:00, 18:00, 23:00")
    print("按 Ctrl+C 停止")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        print("\\n⏹️  定时调度器已停止")

def install_dependencies():
    """安装依赖"""
    print("📦 安装Python依赖...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'requests', 'schedule'], check=True)
        print("✅ 依赖安装完成")
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败")

def show_status():
    """显示状态"""
    print("📊 爬虫系统状态")
    print("=" * 40)
    
    # 检查文件
    files_to_check = [
        "crawler/simple_crawler.py",
        "crawler/config.py", 
        "index.html",
        "style.css"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            
    # 检查数据目录
    data_dir = "crawler/data"
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        print(f"📁 数据文件: {len(files)} 个")
        
        # 显示最新的几个文件
        json_files = [f for f in files if f.endswith('.json')]
        if json_files:
            latest_json = max(json_files, key=lambda f: os.path.getctime(os.path.join(data_dir, f)))
            print(f"📄 最新数据: {latest_json}")
    else:
        print("📁 数据目录不存在")

def main():
    parser = argparse.ArgumentParser(description='英国优惠爬虫管理工具')
    parser.add_argument('action', choices=[
        'run', 'schedule', 'update', 'install', 'status'
    ], help='要执行的操作')
    
    args = parser.parse_args()
    
    print("🚀 英国优惠爬虫管理工具")
    print("=" * 40)
    
    if args.action == 'run':
        print("🔄 立即运行爬虫...")
        success = run_simple_crawler()
        if success:
            update_website()
            
    elif args.action == 'schedule':
        start_scheduler()
        
    elif args.action == 'update':
        print("🔄 更新网站内容...")
        update_website()
        
    elif args.action == 'install':
        install_dependencies()
        
    elif args.action == 'status':
        show_status()

if __name__ == "__main__":
    # 如果没有参数，显示交互式菜单
    if len(sys.argv) == 1:
        print("🚀 英国优惠爬虫管理工具")
        print("=" * 40)
        print("1. 立即运行爬虫")
        print("2. 启动定时调度器")
        print("3. 更新网站内容")
        print("4. 安装依赖")
        print("5. 查看状态")
        print("6. 退出")
        
        while True:
            try:
                choice = input("\\n请选择操作 (1-6): ").strip()
                
                if choice == '1':
                    run_simple_crawler()
                    update_website()
                elif choice == '2':
                    start_scheduler()
                elif choice == '3':
                    update_website()
                elif choice == '4':
                    install_dependencies()
                elif choice == '5':
                    show_status()
                elif choice == '6':
                    print("👋 再见!")
                    break
                else:
                    print("❌ 无效选择")
                    
            except KeyboardInterrupt:
                print("\\n👋 再见!")
                break
    else:
        main()
