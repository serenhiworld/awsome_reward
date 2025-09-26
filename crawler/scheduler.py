import schedule
import time
import os
import sys
from datetime import datetime
from crawler import LatestFreeStuffCrawler
import logging

class CrawlerScheduler:
    def __init__(self):
        self.crawler = LatestFreeStuffCrawler()
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scheduler.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def run_crawler(self):
        """运行爬虫任务"""
        self.logger.info("定时任务启动 - 开始爬取优惠信息")
        
        try:
            deals = self.crawler.crawl_and_translate()
            
            if deals:
                self.logger.info(f"定时任务完成 - 成功处理 {len(deals)} 个优惠信息")
                # 可以在这里添加更新网站的逻辑
                self.update_website(deals)
            else:
                self.logger.warning("定时任务完成 - 未获取到优惠信息")
                
        except Exception as e:
            self.logger.error(f"定时任务失败: {e}")

    def update_website(self, deals):
        """更新网站内容"""
        try:
            # 生成新的优惠内容HTML
            html_content = self.crawler.generate_html_content(deals)
            
            # 将内容插入到主网站
            self.insert_deals_into_website(html_content)
            
            self.logger.info("网站内容更新成功")
            
        except Exception as e:
            self.logger.error(f"更新网站失败: {e}")

    def insert_deals_into_website(self, deals_html):
        """将优惠信息插入到主网站"""
        # 读取主网站HTML文件
        main_html_path = "../index.html"
        
        if not os.path.exists(main_html_path):
            self.logger.error("主网站HTML文件不存在")
            return
            
        with open(main_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 查找插入位置（在推荐产品section后）
        insert_marker = '<section id="benefits" class="benefits">'
        
        if insert_marker in content:
            # 创建新的deals section
            deals_section = f"""
    <section class="daily-deals">
        <div class="container">
            {deals_html}
        </div>
    </section>

    """
            
            # 插入content
            content = content.replace(insert_marker, deals_section + insert_marker)
            
            # 备份原文件
            backup_path = f"../index_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            # 写入更新后的内容
            with open(main_html_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            self.logger.info(f"已更新主网站，备份文件: {backup_path}")
        else:
            self.logger.error("未找到插入位置标记")

    def start_scheduler(self):
        """启动定时调度器"""
        self.logger.info("启动爬虫定时调度器...")
        
        # 每天上午9点运行
        schedule.every().day.at("09:00").do(self.run_crawler)
        
        # 每天下午6点运行
        schedule.every().day.at("18:00").do(self.run_crawler)
        
        # 每天晚上11点运行
        schedule.every().day.at("23:00").do(self.run_crawler)
        
        # 立即运行一次
        self.logger.info("立即运行一次爬虫...")
        self.run_crawler()
        
        # 保持运行
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次

def main():
    """主函数"""
    scheduler = CrawlerScheduler()
    
    try:
        scheduler.start_scheduler()
    except KeyboardInterrupt:
        print("\\n停止调度器...")
        sys.exit(0)

if __name__ == "__main__":
    main()
