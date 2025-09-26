# 爬虫配置文件

# 目标网站配置
TARGET_URL = "https://www.latestfreestuff.co.uk"
MAX_DEALS_PER_RUN = 10
REQUEST_DELAY = 2  # 请求间隔秒数

# 翻译配置
TRANSLATION_SERVICE = "googletrans"  # 可选: googletrans, baidu, tencent
MAX_TRANSLATION_RETRIES = 3
TRANSLATION_DELAY = 1  # 翻译间隔秒数

# 调度配置
SCHEDULE_TIMES = ["09:00", "18:00", "23:00"]  # 每天运行时间
TIMEZONE = "UTC"

# 文件路径配置
DATA_DIR = "data"
LOG_DIR = "logs"
BACKUP_DIR = "backups"
MAIN_WEBSITE_PATH = "../index.html"

# 网站更新配置
AUTO_UPDATE_WEBSITE = True
BACKUP_BEFORE_UPDATE = True
INSERT_POSITION_MARKER = '<section id="benefits" class="benefits">'

# 请求头配置
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
MAX_LOG_SIZE_MB = 10
BACKUP_COUNT = 5
