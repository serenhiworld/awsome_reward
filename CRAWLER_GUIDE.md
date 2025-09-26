# 英国优惠爬虫系统使用指南

## 🎯 系统概述

这个爬虫系统可以自动从 https://www.latestfreestuff.co.uk/ 获取最新的英国优惠信息，翻译成中文并自动更新到您的推荐码网站上。

## 📁 文件结构

```
awsome_reward/
├── index.html                 # 主网站
├── style.css                  # 主网站样式
├── script.js                  # 主网站脚本
├── manage_crawler.py          # 爬虫管理工具
├── crawler/
│   ├── simple_crawler.py      # 简化版爬虫
│   ├── crawler.py             # 完整版爬虫
│   ├── scheduler.py           # 定时调度器
│   ├── config.py              # 配置文件
│   ├── requirements.txt       # Python依赖
│   ├── run.sh                 # Linux启动脚本
│   └── data/                  # 爬取数据存储
└── README.md                  # 项目说明
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装基础依赖
pip install requests schedule

# 或安装完整依赖（可选）
cd crawler
pip install -r requirements.txt
```

### 2. 运行爬虫

#### 方法一：使用管理工具（推荐）
```bash
python3 manage_crawler.py
```
然后选择相应的操作：
- 1: 立即运行爬虫
- 2: 启动定时调度器  
- 3: 更新网站内容
- 4: 安装依赖
- 5: 查看状态

#### 方法二：直接运行
```bash
# 立即运行一次爬虫
cd crawler
python3 simple_crawler.py

# 启动定时调度器
python3 scheduler.py
```

#### 方法三：使用Shell脚本（Linux）
```bash
cd crawler
chmod +x run.sh
./run.sh
```

## ⚙️ 配置选项

编辑 `crawler/config.py` 文件可以修改以下配置：

```python
# 目标网站
TARGET_URL = "https://www.latestfreestuff.co.uk"

# 爬取数量限制
MAX_DEALS_PER_RUN = 10

# 定时任务时间
SCHEDULE_TIMES = ["09:00", "18:00", "23:00"]

# 是否自动更新网站
AUTO_UPDATE_WEBSITE = True
```

## 🔄 工作流程

1. **爬取数据**: 从目标网站获取最新优惠信息
2. **数据清理**: 提取标题、描述、链接等关键信息
3. **翻译内容**: 将英文内容翻译成中文
4. **保存数据**: 保存为JSON和HTML格式
5. **更新网站**: 自动将内容插入到主网站

## 📊 数据格式

### JSON格式
```json
{
  "title": "Free Sample Box",
  "title_zh": "免费样品盒",
  "description": "Get a free sample box...",
  "description_zh": "获得免费样品盒...",
  "url": "https://example.com/deal",
  "image": "https://example.com/image.jpg",
  "date": "2024-03-20"
}
```

### HTML输出
生成的HTML会自动插入到网站的指定位置，包含：
- 优惠标题（中文）
- 优惠描述（中文）
- 查看详情链接
- 发布日期

## 🎨 样式定制

优惠内容的样式已经集成到主网站的 `style.css` 中，包括：

- `.daily-deals-section`: 整体容器样式
- `.deal-item`: 单个优惠项样式
- `.deal-link`: 查看详情按钮样式
- 响应式设计支持

您可以修改这些样式来匹配网站的整体设计。

## 🕒 定时任务

系统支持自动定时运行，默认时间：
- 上午 09:00
- 下午 18:00  
- 晚上 23:00

### 后台运行
```bash
# Linux/Mac 后台运行
nohup python3 manage_crawler.py schedule > crawler.log 2>&1 &

# 查看运行状态
ps aux | grep manage_crawler

# 停止后台进程
pkill -f manage_crawler
```

## 📝 日志管理

系统会自动生成日志文件：
- `simple_crawler.log`: 爬虫运行日志
- `scheduler.log`: 定时任务日志  
- `crawler.log`: 详细运行日志

### 查看日志
```bash
# 查看最新日志
tail -f simple_crawler.log

# 查看特定行数
tail -50 simple_crawler.log
```

## 🛠️ 故障排除

### 常见问题

1. **网站连接失败**
   - 检查网络连接
   - 确认目标网站是否可访问
   - 检查请求头设置

2. **翻译失败**
   - 简化版使用基础词汇替换
   - 完整版需要配置翻译API
   - 检查翻译服务配置

3. **网站更新失败**
   - 检查HTML文件路径
   - 确认插入标记存在
   - 检查文件权限

### 调试模式
```bash
# 测试网站连接
python3 -c "
from crawler.simple_crawler import SimpleFreeStuffCrawler
crawler = SimpleFreeStuffCrawler()
content = crawler.get_page_content('https://www.latestfreestuff.co.uk')
print('连接成功' if content else '连接失败')
"

# 测试爬虫功能
cd crawler
python3 simple_crawler.py
```

## 🔧 高级配置

### 自定义翻译服务

如需使用专业翻译API，可以修改 `simple_crawler.py` 中的翻译部分：

```python
def translate_to_chinese(self, text):
    # 替换为您的翻译API调用
    # 例如：百度翻译、腾讯翻译等
    pass
```

### 添加更多网站

在 `crawler.py` 中可以添加多个目标网站：

```python
websites = [
    "https://www.latestfreestuff.co.uk",
    "https://www.hotukdeals.com",
    # 添加更多网站
]
```

## 📈 性能优化

- 设置合理的请求间隔避免被封IP
- 使用缓存减少重复翻译
- 限制爬取数量避免过载
- 定期清理旧数据文件

## ⚠️ 使用注意事项

1. **遵守robots.txt**: 尊重目标网站的爬取规则
2. **适度爬取**: 不要过于频繁地访问目标网站
3. **数据验证**: 定期检查爬取数据的质量
4. **备份重要数据**: 定期备份网站和数据文件
5. **监控运行状态**: 关注日志文件中的错误信息

## 🆘 技术支持

如遇问题，请：
1. 查看日志文件了解错误详情
2. 检查网络连接和目标网站状态  
3. 确认Python环境和依赖正确安装
4. 参考本文档的故障排除部分

---

🎉 **祝您使用愉快！通过自动化爬虫，让您的推荐码网站内容更丰富、更及时！**
