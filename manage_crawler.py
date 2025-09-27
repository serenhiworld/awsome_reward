#!/usr/bin/env python3
"""
英国优惠爬虫管理工具
支持立即运行、定时调度、网站更新等功能
"""

import os
import sys
import subprocess
import schedule
import time
from datetime import datetime
import argparse

from update_website import WebsiteUpdater

DEFAULT_CRAWLER = "enhanced"
CRAWLER_SCRIPTS = {
    "enhanced": "enhanced_crawler.py",
    "simple": "simple_crawler.py",
}


def run_crawler(mode: str = DEFAULT_CRAWLER) -> bool:
    """运行指定版本的每日优惠爬虫"""
    script_name = CRAWLER_SCRIPTS.get(mode, CRAWLER_SCRIPTS[DEFAULT_CRAWLER])
    human_label = "增强" if mode == "enhanced" else "基础"
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            cwd="crawler",
        )
        if result.returncode == 0:
            print(f"✅ {human_label}爬虫运行成功")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {human_label}爬虫运行失败")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as exc:
        print(f"❌ 运行{human_label}爬虫时出错: {exc}")
        return False


def update_website() -> bool:
    """调用网站更新工具，将最新爬虫数据写入首页"""
    try:
        updater = WebsiteUpdater()
        if updater.update_from_latest_data():
            print("✅ 网站内容已更新")
            return True
        return False
    except Exception as exc:
        print(f"❌ 更新网站时出错: {exc}")
        return False


def scheduled_task(crawler_mode: str = DEFAULT_CRAWLER):
    """定时任务"""
    print(f"\n🕒 定时任务开始 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if run_crawler(crawler_mode):
        update_website()
        print("✅ 定时任务完成")
    else:
        print("❌ 定时任务失败")


def start_scheduler(crawler_mode: str = DEFAULT_CRAWLER):
    """启动定时调度器"""
    print("⏰ 启动定时调度器...")

    schedule.every().day.at("09:00").do(scheduled_task, crawler_mode=crawler_mode)
    schedule.every().day.at("18:00").do(scheduled_task, crawler_mode=crawler_mode)
    schedule.every().day.at("23:00").do(scheduled_task, crawler_mode=crawler_mode)

    print("🔄 立即运行一次...")
    scheduled_task(crawler_mode)

    print("⏰ 时调度器已启动，等待定时任务...")
    print("📅 调度时间: 09:00, 18:00, 23:00")
    print("按 Ctrl+C 停止")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n⏹️  定时调度器已停止")


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

    files_to_check = [
        "crawler/simple_crawler.py",
        "crawler/enhanced_crawler.py",
        "crawler/config.py",
        "crawler/enhanced_config.py",
        "index.html",
        "style.css"
    ]

    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")

    data_dir = "crawler/data"
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        print(f"📁 数据文件: {len(files)} 个")

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
    parser.add_argument(
        '--crawler',
        choices=sorted(CRAWLER_SCRIPTS.keys()),
        default=DEFAULT_CRAWLER,
        help='选择运行的爬虫版本（默认: enhanced）'
    )

    args = parser.parse_args()

    print("🚀 英国优惠爬虫管理工具")
    print("=" * 40)

    if args.action == 'run':
        print("🔄 立即运行爬虫...")
        success = run_crawler(args.crawler)
        if success:
            update_website()

    elif args.action == 'schedule':
        start_scheduler(args.crawler)

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
        print("1. 立即运行增强版爬虫")
        print("2. 立即运行基础版爬虫")
        print("3. 启动定时调度器 (增强版)")
        print("4. 启动定时调度器 (基础版)")
        print("5. 更新网站内容")
        print("6. 安装依赖")
        print("7. 查看状态")
        print("8. 退出")

        while True:
            try:
                choice = input("\n请选择操作 (1-8): ").strip()

                if choice == '1':
                    run_crawler('enhanced')
                    update_website()
                elif choice == '2':
                    run_crawler('simple')
                    update_website()
                elif choice == '3':
                    start_scheduler('enhanced')
                elif choice == '4':
                    start_scheduler('simple')
                elif choice == '5':
                    update_website()
                elif choice == '6':
                    install_dependencies()
                elif choice == '7':
                    show_status()
                elif choice == '8':
                    print("👋 再见!")
                    break
                else:
                    print("❌ 无效选择")

            except KeyboardInterrupt:
                print("\n👋 再见!")
                break
    else:
        main()
