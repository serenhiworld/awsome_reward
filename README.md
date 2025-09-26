# 🎯 英国优惠推荐码分享网站

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://serenhiworld.github.io/awsome_reward)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Automation](https://img.shields.io/badge/Automation-✅-green)]()

> 一个面向在英华人的中文优惠推荐码分享网站，实现自动每日爬取英国最新优惠信息，自动翻译并发布到网站，支持GitHub Pages部署。

## 🌟 在线预览

**网站地址**: [https://serenhiworld.github.io/awsome_reward](https://serenhiworld.github.io/awsome_reward)

## ✨ 核心功能

### 🤖 全自动化流程
- **自动爬虫**: 每日自动爬取 latestfreestuff.co.uk 最新优惠信息
- **智能提取**: 深度提取真实外部商家链接（非中间跳转链接）
- **自动翻译**: 英文内容自动翻译成中文
- **网站更新**: 自动更新网站内容，实时展示最新优惠
- **报告生成**: 自动生成爬取和更新报告

### � 网站特性
- **响应式设计**: 完美适配桌面端和移动端
- **中文界面**: 专为在英华人设计的中文用户界面
- **推荐码集成**: 内置Virgin Media、Octopus Energy等推荐码
- **真实链接**: 显示真实的商家外部链接，提高转化率
- **SEO优化**: 包含sitemap、robots.txt等SEO配置

### 🚀 快速部署
- **GitHub Pages**: 支持一键部署到GitHub Pages
- **自动更新**: 可配置定时任务自动运行
- **零成本**: 完全免费的托管解决方案

## 当前推荐码分享

### 🌐 Virgin Media 宽带推荐码
- **我的推荐链接**: https://aklam.io/vBZtH2
- **学生专享优惠**: https://www.virginmedia.com/broadband/student
- **双赢收益**: 
  - ✅ 您享受学生12个月大优惠
  - ✅ 我获得推荐佣金奖励
  - ✅ 超快光纤宽带服务
  - ✅ 免费专业安装服务

### ⚡ Octopus Energy 电力推荐码
- **我的推荐链接**: https://share.octopus.energy/harsh-fish-37
- **现金奖励**: 双方各获得£50现金奖励
- **双赢收益**:
## 📁 项目结构

```
awsome_reward/
├── 📄 index.html              # 主网站页面
├── 🎨 style.css               # 网站样式
├── ⚡ script.js               # 网站交互脚本
├── 🤖 automation.py           # 全自动化主脚本
├── 🔧 manage_crawler.py       # 爬虫管理脚本
├── 📝 update_website.py       # 网站内容更新脚本
├── 📊 crawler/                # 爬虫系统目录
│   ├── enhanced_crawler.py    # 增强版爬虫（主爬虫）
│   ├── enhanced_config.py     # 爬虫配置文件
│   ├── config.py              # 基础配置
│   ├── requirements.txt       # Python依赖
│   └── data/                  # 爬取数据存储
├── 🚀 deploy.sh               # 部署脚本
├── 📋 sitemap.xml             # SEO站点地图
├── 🤖 robots.txt              # 搜索引擎爬虫配置
└── 📚 文档/                   # 项目文档
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <your-repo-url>
cd awsome_reward

# 安装Python依赖
pip install -r crawler/requirements.txt
```

### 2. 一键运行全自动化

```bash
# 运行全自动化流程：爬虫→翻译→更新网站→生成报告
python automation.py

# 可选参数:
python automation.py --max-deals 10    # 指定最大爬取数量
python automation.py --no-update       # 只运行爬虫，不更新网站
python automation.py --force-update    # 强制更新网站（即使没有新数据）
```

### 3. 单独运行模块

```bash
# 只运行爬虫
python manage_crawler.py

# 只更新网站内容
python update_website.py

# 直接运行增强版爬虫
cd crawler
python enhanced_crawler.py
```

### 4. 本地预览网站

```bash
# 启动本地服务器
python -m http.server 8000

# 在浏览器中访问
http://localhost:8000
```

## 🤖 爬虫系统详解

### 核心特性

#### 🎯 真实链接提取
- **多层深度提取**: 不仅获取列表页链接，还会点进详情页和claim页
- **智能识别**: 自动识别并提取真实的外部商家链接
- **过滤机制**: 过滤掉中间跳转链接，直达商家网站

#### 🌍 自动翻译
- **标题翻译**: 英文标题自动翻译成中文
- **描述翻译**: 优惠描述自动翻译成中文
- **缓存机制**: 翻译结果缓存，提高效率

#### 📊 数据处理
- **结构化存储**: 优惠数据以JSON格式结构化存储
- **时间戳**: 每次爬取都有时间戳记录
- **数据清洗**: 自动去重和数据验证

### 配置说明

```python
# crawler/enhanced_config.py
BASE_URL = "https://www.latestfreestuff.co.uk"  # 目标网站
MAX_DEALS = 10                                  # 最大爬取数量
REQUEST_DELAY = 2                               # 请求间隔（秒）
ENABLE_TRANSLATION = True                       # 是否启用翻译
```

### 数据输出格式

```json
{
  "timestamp": "2024-01-15 10:30:00",
  "deals": [
    {
      "title": "Free Sample from XYZ",
      "title_zh": "XYZ免费样品",
      "description": "Get free sample...",
      "description_zh": "获取免费样品...",
      "url": "https://xyz.com/free-sample",
      "source_url": "https://latestfreestuff.co.uk/deal/xyz",
      "image": "https://xyz.com/image.jpg",
      "date": "2024-01-15",
      "domain": "xyz.com"
    }
  ]
}
```

## 🚀 部署指南

### GitHub Pages 部署

#### 1. 推送到GitHub

```bash
# 初始化Git仓库（如果还没有）
git init
git add .
git commit -m "Initial commit"

# 添加远程仓库
git remote add origin https://github.com/yourusername/awsome_reward.git
git push -u origin main
```

#### 2. 启用GitHub Pages

1. 进入GitHub仓库设置
2. 找到"Pages"选项
3. 选择"Deploy from a branch"
4. 选择"main"分支
5. 选择"/ (root)"目录
6. 点击"Save"

#### 3. 自动部署脚本

```bash
# 使用内置部署脚本
chmod +x deploy.sh
./deploy.sh
```

### 定时任务设置

#### Linux/Mac Crontab

```bash
# 编辑crontab
crontab -e

# 添加每日8点自动运行
0 8 * * * cd /path/to/awsome_reward && python automation.py >> automation.log 2>&1
```

#### GitHub Actions

创建 `.github/workflows/daily-update.yml`:

```yaml
name: Daily Update
on:
  schedule:
    - cron: '0 8 * * *'  # 每日8点UTC
  workflow_dispatch:     # 手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: pip install -r crawler/requirements.txt
    - name: Run automation
      run: python automation.py
    - name: Commit changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add .
        git commit -m "Daily update $(date)" || exit 0
        git push
```

## 🔧 配置与自定义

### 爬虫配置

```python
# crawler/enhanced_config.py 主要配置项

# 基础设置
BASE_URL = "https://www.latestfreestuff.co.uk"
MAX_DEALS = 10
REQUEST_DELAY = 2

# 翻译设置
ENABLE_TRANSLATION = True
TRANSLATION_CACHE_SIZE = 1000

# 数据过滤
MIN_TITLE_LENGTH = 5
MAX_TITLE_LENGTH = 200
EXCLUDE_KEYWORDS = ['spam', 'expired']
```

### 网站自定义

```html
<!-- 添加新的推荐码 (index.html) -->
<div class="referral-card">
    <h3>🏠 新服务推荐码</h3>
    <div class="referral-content">
        <p><strong>推荐码:</strong> <span class="code">NEWCODE123</span></p>
        <p><strong>优惠:</strong> 新用户获得特殊折扣</p>
        <a href="https://newservice.com" class="btn btn-primary" target="_blank">
            立即使用
        </a>
    </div>
</div>
```

## 📊 运行日志与监控

### 日志文件

```
automation.log           # 自动化运行日志
crawler/enhanced_crawler.log  # 爬虫详细日志
```

### 监控指标

- 每日爬取数据量
- 翻译成功率
- 网站更新状态
- 错误率统计

## � 故障排除

### 常见问题

#### 1. 爬虫无法获取数据
```bash
# 检查网络连接
curl -I https://www.latestfreestuff.co.uk

# 检查依赖安装
pip install -r crawler/requirements.txt

# 查看错误日志
tail -f crawler/enhanced_crawler.log
```

#### 2. 网站内容未更新
```bash
# 手动运行更新
python update_website.py

# 检查数据文件
ls -la crawler/data/

# 检查权限
chmod +x automation.py
```

## � 依赖说明

### Python依赖 (requirements.txt)
```
requests>=2.28.0     # HTTP请求
beautifulsoup4>=4.11.0  # HTML解析
lxml>=4.9.0          # XML/HTML解析器
```

## 🔒 安全考虑

### 爬虫礼貌性
- 设置合理的请求间隔
- 遵守robots.txt
- 设置User-Agent

### 数据安全
- 不存储敏感信息
- 定期清理旧数据
- 输入验证和过滤

## 📞 支持与贡献

### 推荐码服务
- **Virgin Media 宽带** - 学生专享12个月优惠
- **Octopus Energy 电力** - 双方各获得£50奖励
- **透明诚信** - 明确说明推荐码性质

### 问题反馈
- 通过GitHub Issues提交问题
- 提供详细的错误信息和日志

## 📄 许可证

本项目采用MIT许可证，详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢 latestfreestuff.co.uk 提供优惠信息
- 感谢开源社区的各种工具和库
- 感谢所有贡献者和用户的支持

---

**💡 提示**: 这是一个完全自动化的系统，设置完成后可以实现每日自动更新，为在英华人提供最新的优惠信息！

© 2024 英国优惠推荐码分享网站. 透明诚信，互惠共赢.
