# 🚀 快速部署到GitHub指南

## 方法一：使用自动化脚本（推荐）

1. **运行部署脚本**：
   ```bash
   ./deploy.sh
   ```
   
2. **按提示输入信息**：
   - GitHub用户名
   - 仓库名称（默认：uk-deals-referral）
   - 邮箱地址

3. **在GitHub创建仓库**：
   - 访问 https://github.com/new
   - 输入仓库名称
   - 设置为Public
   - 点击"Create repository"

4. **完成推送**：
   脚本会自动推送代码到GitHub

## 方法二：手动部署

1. **在GitHub创建仓库**
2. **推送代码**：
   ```bash
   git remote add origin https://github.com/your-username/uk-deals-referral.git
   git branch -M main
   git push -u origin main
   ```

3. **配置GitHub Pages**：
   - 进入仓库Settings → Pages
   - Source选择"Deploy from a branch"
   - Branch选择"main"
   - 点击Save

## 🌐 访问网站

部署完成后，您的网站将在以下地址访问：
```
https://your-username.github.io/uk-deals-referral
```

## 🔄 自动更新

- 每次推送到main分支都会自动部署
- GitHub Actions会自动运行爬虫更新内容
- 无需手动维护

## 📞 需要帮助？

查看详细文档：
- 📖 [部署指南](DEPLOY_GUIDE.md)
- 🤖 [爬虫指南](CRAWLER_GUIDE.md)
- 📊 [项目总结](PROJECT_SUMMARY.md)
