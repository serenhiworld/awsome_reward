# 增强爬虫配置文件
# Enhanced Crawler Configuration

# 基础配置
BASE_URL = "https://www.latestfreestuff.co.uk"
MAX_DEALS = 20  # 最大获取的优惠数量
REQUEST_DELAY = 2  # 请求间隔（秒）
REQUEST_TIMEOUT = 30  # 请求超时（秒）

# 请求头配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Referer': 'https://www.latestfreestuff.co.uk',
}

# 文件路径配置
DATA_DIR = "data"
OUTPUT_FILE = "deals.json"
HTML_OUTPUT = "../index.html"

# 翻译配置
ENABLE_TRANSLATION = True

# 真实链接提取配置
REAL_LINK_EXTRACTION = {
    'enabled': True,
    'max_retries': 3,  # 最大重试次数
    'timeout': 15,     # 单个链接提取超时
    
    # 主要链接模式（按优先级排序）
    'primary_patterns': [
        r'<a[^>]+class=["\'][^"\']*(?:deal-btn|offer-btn|get-deal|visit-store|claim-deal|btn-primary)[^"\']*["\'][^>]+href=["\']([^"\']+)["\']',
        r'<a[^>]+target=["\']_blank["\'][^>]+href=["\']([^"\']+)["\']',
        r'<a[^>]+href=["\']([^"\']+)["\'][^>]+target=["\']_blank["\']',
        r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>[^<]*(?:Get Deal|Visit Store|Claim Deal|Shop Now|Get Offer|Grab Deal)[^<]*</a>',
        r'<a[^>]+rel=["\']nofollow["\'][^>]+href=["\']([^"\']+)["\']',
        r'<a[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']nofollow["\']',
    ],
    
    # 次要链接模式
    'secondary_patterns': [
        r'<a[^>]+class=["\'][^"\']*(?:btn|button)[^"\']*["\'][^>]+href=["\']([^"\']+)["\']',
        r'href=["\']([^"\']*(?:deal|offer|promo|discount)[^"\']*)["\']',
        r'href=["\']([^"\']*(?:go|visit|redirect)[^"\']*)["\']',
        r'href=["\']((https?://(?!(?:www\.)?latestfreestuff\.co\.uk)[a-zA-Z0-9][^"\']*?))["\']'
    ],
    
    # JavaScript重定向模式
    'js_patterns': [
        r'window\.location\.href\s*=\s*["\']([^"\']+)["\']',
        r'window\.location\s*=\s*["\']([^"\']+)["\']',
        r'location\.href\s*=\s*["\']([^"\']+)["\']',
        r'document\.location\s*=\s*["\']([^"\']+)["\']',
    ],
}

# URL验证配置
URL_VALIDATION = {
    # 排除的URL模式
    'invalid_patterns': [
        'javascript:', 'mailto:', '#', 'latestfreestuff.co.uk',
        '/terms', '/privacy', '/about', '/contact', '/login', '/register', '/search',
        'facebook.com/sharer', 'twitter.com/intent', 'instagram.com',
        'youtube.com', 'linkedin.com/sharing', 'pinterest.com/pin',
        'google.com/search', 'bing.com/search', 'yahoo.com/search',
    ],
    
    # 排除的文件扩展名
    'invalid_extensions': ['.pdf', '.doc', '.docx', '.zip', '.rar', '.exe', '.dmg'],
    
    # 可信的购物网站域名
    'trusted_domains': [
        'amazon.co.uk', 'amazon.com', 'ebay.co.uk', 'ebay.com',
        'argos.co.uk', 'currys.co.uk', 'johnlewis.com', 'marksandspencer.com',
        'tesco.com', 'asda.com', 'sainsburys.co.uk', 'morrisons.com',
        'boots.com', 'superdrug.com', 'next.co.uk', 'hm.com',
        'zara.com', 'asos.com', 'boohoo.com', 'prettylittlething.com',
        'topshop.com', 'newlook.com', 'primark.com', 'tkmaxx.com',
        'virginmedia.com', 'octopus.energy', 'bulb.co.uk', 'edf.co.uk',
        'groupon.co.uk', 'wowcher.co.uk', 'vouchercodes.co.uk',
        'hotukdeals.com', 'myvouchercodes.co.uk', 'retailmenot.com',
        'expedia.co.uk', 'booking.com', 'hotels.com', 'lastminute.com',
        'ryanair.com', 'easyjet.com', 'ba.com', 'trainline.com',
        'mcdonalds.co.uk', 'kfc.co.uk', 'pizzahut.co.uk', 'dominos.co.uk',
        'spotify.com', 'netflix.com', 'disneyplus.com', 'audible.co.uk',
    ],
    
    # 优惠相关关键词
    'deal_keywords': [
        'deal', 'offer', 'discount', 'coupon', 'promo', 'sale',
        'shop', 'store', 'buy', 'checkout', 'cart', 'order',
        'voucher', 'code', 'cashback', 'reward', 'special',
        'limited', 'exclusive', 'bonus', 'gift', 'free'
    ]
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'enhanced_crawler.log',
    'max_bytes': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}
