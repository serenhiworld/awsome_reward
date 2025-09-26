# 📋 GitHub仓库创建和推送指南

## 🎯 方法一：使用密码推送脚本（推荐）

1. **运行推送脚本**：
   ```bash
   ./push_with_password.sh
   ```

2. **输入GitHub信息**：
   - GitHub用户名：`serenhiworld`
   - GitHub密码：您的GitHub密码

3. **自动推送**：脚本会自动推送代码到GitHub

## 🔧 方法二：手动创建和推送

### 步骤1：在GitHub创建仓库
1. 访问：https://github.com/new
2. 仓库名称：`awsome_reward`
3. 描述：`英国优惠推荐码分享网站`
4. 设置为：**Public**（必须，否则无法使用免费的GitHub Pages）
5. **不要**勾选"Initialize this repository with a README"
6. 点击"Create repository"

### 步骤2：推送代码
```bash
# 设置带密码的远程仓库地址
git remote set-url origin https://serenhiworld:YOUR_PASSWORD@github.com/serenhiworld/awsome_reward.git

# 推送代码
git push -u origin main
```

### 步骤3：配置GitHub Pages
1. 访问：https://github.com/serenhiworld/awsome_reward/settings/pages
2. **Source**：选择"Deploy from a branch"
3. **Branch**：选择"main"
4. **Folder**：选择"/ (root)"
5. 点击"**Save**"

## 🌐 访问网站
配置完成后，您的网站将在以下地址可访问：
```
https://serenhiworld.github.io/awsome_reward
```

## ⚠️ 安全提示

使用密码推送时注意：
1. **不要在公共电脑上保存密码**
2. **定期更换GitHub密码**
3. **考虑启用两步验证**

## 🆘 常见问题

### Q: 推送时提示403错误
**A**: 检查用户名和密码是否正确，确保仓库已创建

### Q: GitHub Pages不工作
**A**: 
- 确保仓库是Public
- 检查Pages设置是否正确
- 等待几分钟让GitHub处理

### Q: 网站显示404
**A**: 
- 确保index.html在根目录
- 检查文件名是否正确
- 等待Pages部署完成

## 📞 需要帮助？

如果遇到问题：
1. 检查GitHub仓库是否创建成功
2. 确认用户名密码正确
3. 查看终端错误信息
4. 参考GitHub官方文档
