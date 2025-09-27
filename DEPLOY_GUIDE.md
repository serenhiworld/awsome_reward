# 🚀 部署到GitHub Pages指南

本指南将帮助您将项目部署到GitHub，并使用GitHub Pages展示网站。

## 📋 准备工作

1. **GitHub账号** - 确保您有GitHub账号
2. **Git工具** - 本地安装Git命令行工具
3. **项目文件** - 确保所有文件都已准备好

## 🔧 步骤一：创建GitHub仓库

### 1. 登录GitHub
前往 [github.com](https://github.com) 并登录您的账号

### 2. 创建新仓库
- 点击右上角的 "+" 号，选择 "New repository"
- **仓库名称**: `uk-deals-referral` (或您喜欢的名称)
- **描述**: "英国优惠推荐码分享网站 - 互惠共赢的透明推荐平台"
- 选择 **Public** (公开仓库，免费使用GitHub Pages)
- **不要**勾选 "Initialize this repository with a README"
- 点击 "Create repository"

## 📤 步骤二：上传代码到GitHub

### 1. 初始化Git仓库
在项目目录中运行：
```bash
cd /home/ke/Documents/refer/awsome_reward
git init
git add .
git commit -m "Initial commit: UK deals referral website with crawler system"
```

### 2. 连接到GitHub仓库
```bash
# 将your-username替换为您的GitHub用户名
git remote add origin https://github.com/your-username/uk-deals-referral.git
git branch -M main
git push -u origin main
```

### 3. 推送代码
```bash
git push origin main
```

## 🌐 步骤三：配置GitHub Pages

### 1. 进入仓库设置
- 在GitHub仓库页面，点击 "Settings" 标签
- 在左侧菜单中找到 "Pages"

### 2. 配置Pages设置
- **Source**: 选择 "Deploy from a branch"
- **Branch**: 选择 "main"
- **Folder**: 选择 "/ (root)"
- 点击 "Save"

### 3. 等待部署
- GitHub会自动构建和部署网站
- 通常需要几分钟时间
- 部署成功后会显示网站地址

## ✅ 步骤四：验证部署

### 1. 访问网站
部署完成后，您的网站将在以下地址可访问：
```
https://your-username.github.io/uk-deals-referral
```

### 2. 检查功能
- ✅ 网站正常加载
- ✅ 响应式设计工作正常
- ✅ 推荐链接可以点击
- ✅ 所有样式和动画正常

## 🔧 步骤五：自定义域名（可选）

### 1. 添加CNAME文件
如果您有自己的域名，创建 `CNAME` 文件：
```bash
echo "yourdomain.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push origin main
```

### 2. 配置DNS
在您的域名提供商处添加CNAME记录：
```
CNAME  @  your-username.github.io
```

## 🔄 日常更新流程

### 1. 本地修改
```bash
# 编辑文件后
git add .
git commit -m "Update: description of changes"
git push origin main
```

### 2. 自动部署
- 每次推送到main分支都会自动触发部署
- 等待几分钟即可看到更新

## 📊 GitHub Actions自动化（进阶）

创建 `.github/workflows/deploy.yml` 实现自动化：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
        
    - name: Install dependencies
      run: |
        pip install requests
        
    - name: Run crawler (optional)
      run: |
        python manage_crawler.py crawl
        
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
```

## 🛠️ 常见问题解决

### 问题1: 推送被拒绝
```bash
# 强制推送（谨慎使用）
git push -f origin main
```

### 问题2: Pages没有更新
- 检查Actions标签页是否有构建错误
- 清除浏览器缓存
- 等待几分钟后重试

### 问题3: 样式不显示
确保CSS和JS文件路径正确：
```html
<link rel="stylesheet" href="./style.css">
<script src="./script.js"></script>
```

## 🎯 SEO优化

### 1. 添加meta标签
在 `index.html` 的 `<head>` 中添加：
```html
<meta name="description" content="英国优惠推荐码分享，Virgin Media宽带、Octopus Energy电力推荐码，互惠共赢">
<meta name="keywords" content="英国优惠,推荐码,Virgin Media,Octopus Energy,留学生">
<meta property="og:title" content="英国优惠推荐码分享">
<meta property="og:description" content="透明诚信的推荐码分享平台">
<meta property="og:url" content="https://your-username.github.io/uk-deals-referral">
```

### 2. 创建sitemap.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://your-username.github.io/uk-deals-referral</loc>
    <lastmod>2024-03-20</lastmod>
    <priority>1.0</priority>
  </url>
</urlset>
```

## 🚀 完成！

恭喜！您的网站现在已经：
- ✅ 托管在GitHub上
- ✅ 通过GitHub Pages展示
- ✅ 自动部署更新
- ✅ 全球访问

您的推荐码分享网站现在可以在全世界访问了！🎉
