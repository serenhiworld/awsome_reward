#!/usr/bin/env python3
"""轻量化的爬虫管理工具.

该脚本只保留与增强版爬虫相关的实用命令, 用于简化日常操作。
"""

from __future__ import annotations

import argparse
import sys
from typing import Sequence

from automation import AutomationManager


def run_full_workflow(manager: AutomationManager) -> int:
    """Run the complete automation pipeline."""
    success = manager.run_full_automation()
    return 0 if success else 1


def run_crawler_only(manager: AutomationManager) -> int:
    """Execute the crawler and print a short summary."""
    deals = manager.run_crawler()
    if deals:
        print(f"✅ 成功获取 {len(deals)} 个优惠")
        return 0

    print("❌ 未获取到任何优惠，请检查日志或目标网站状态")
    return 1


def update_site(manager: AutomationManager) -> int:
    """Update the website using the freshest data."""
    updated = manager.update_website()
    if updated:
        print("✅ 网站内容更新成功")
        return 0

    print("⚠️ 网站内容未更新，请确认是否存在有效的优惠数据")
    return 1


def generate_report(manager: AutomationManager, deals: int) -> int:
    """Generate a markdown report for the latest run."""
    manager.generate_report(deals)
    print("✅ 报告已生成")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="英国优惠爬虫自动化管理工具",
    )
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser(
        "run", help="运行完整流程: 爬虫 → 更新网站 → 生成报告"
    )
    run_parser.set_defaults(command="run")

    crawl_parser = subparsers.add_parser("crawl", help="仅运行增强版爬虫")
    crawl_parser.set_defaults(command="crawl")

    update_parser = subparsers.add_parser("update", help="根据最新数据更新网站")
    update_parser.set_defaults(command="update")

    report_parser = subparsers.add_parser("report", help="生成运行报告")
    report_parser.add_argument(
        "--deals",
        type=int,
        default=0,
        help="本次运行获取的优惠数量 (默认为0)",
    )
    report_parser.set_defaults(command="report")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    command = args.command or "run"

    manager = AutomationManager()

    if command == "run":
        return run_full_workflow(manager)
    if command == "crawl":
        return run_crawler_only(manager)
    if command == "update":
        return update_site(manager)
    if command == "report":
        deals = getattr(args, "deals", 0)
        return generate_report(manager, deals)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
