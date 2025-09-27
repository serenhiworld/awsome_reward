# 英国优惠爬虫系统使用指南

## 🎯 系统概述

该系统会自动从 https://www.latestfreestuff.co.uk 获取最新优惠信息, 翻译成中文并生成适合展示在网站上的 HTML 内容。核心流程由 `automation.py` 驱动, 并可以通过 `manage_crawler.py` 轻松调用。

## 📁 文件结构

```
awsome_reward/
├── automation.py           # 全流程自动化脚本
├── manage_crawler.py       # 轻量化命令行工具
├── update_website.py       # 基于历史数据更新网站
└── crawler/
    ├── enhanced_crawler.py # 增强版爬虫(核心逻辑)
    ├── enhanced_config.py  # 爬虫配置
    ├── requirements.txt    # Python 依赖
    └── data/               # 爬取结果(JSON/HTML)
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r crawler/requirements.txt
```

### 2. 常用命令

使用 `manage_crawler.py` 可以快速执行不同任务:

```bash
# 运行完整流程: 爬虫 → 更新网站 → 生成报告
python manage_crawler.py run

# 仅运行增强版爬虫
python manage_crawler.py crawl

# 根据最新数据更新网站
python manage_crawler.py update

# 生成运行报告
python manage_crawler.py report --deals 5
```

> 不带任何参数直接运行 `python manage_crawler.py` 也会执行完整流程。

### 3. 直接调用底层脚本(可选)

```bash
# 仅运行增强版爬虫
cd crawler
python enhanced_crawler.py

# 使用最新的数据文件更新网站
python update_website.py
```

## ⚙️ 配置

所有可调参数集中在 `crawler/enhanced_config.py`, 包括:

- `BASE_URL`: 目标网站
- `MAX_DEALS`: 每次抓取的最大优惠数量
- `REQUEST_DELAY`: 请求间隔, 防止触发反爬
- `ENABLE_TRANSLATION`: 是否启用内置的简单翻译
- `REAL_LINK_EXTRACTION`: 真实链接提取规则

修改配置后无需重启, 下次运行爬虫时会自动读取。

## 📊 数据输出

运行爬虫后会在 `crawler/data/` 目录生成两类文件:

- `enhanced_deals_*.json`: 结构化的优惠数据
- `enhanced_deals_*.html`: 可直接嵌入网站的 HTML 片段

`automation.py` 会自动选择最新数据并更新 `index.html` 中的优惠板块。

## 📝 日志

- `automation.log`: 全流程运行日志
- `crawler/enhanced_crawler.log`: 爬虫运行日志

日志有助于排查网络错误、链接提取失败等问题。

## 🛠️ 常见问题

1. **未抓取到优惠**
   - 检查目标网站是否可访问
   - 适当提高 `REQUEST_DELAY`

2. **网站未更新**
   - 确认 `crawler/data/` 中存在最新 JSON/HTML
   - 手动运行 `python manage_crawler.py update`

3. **翻译结果质量不佳**
   - 目前使用简单的词汇替换, 可以在 `SimpleTranslator` 中自定义词典

---

如需进一步自动化(例如定时任务), 建议在外部调度系统中调用 `python manage_crawler.py run`, 无需额外脚本支持。
