# 🚀 Google账号GitHub快速部署

## 📋 适用情况
✅ 您使用Google账号登录GitHub  
✅ 想要免费托管推荐码分享网站  
✅ 需要简单快速的部署方案  

## ⚡ 3分钟快速部署

### 第1步: 创建Token (1分钟)
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 填写名称："UK Referral Website"
4. 勾选权限：`repo`
5. 点击 "Generate token"
6. **立即复制并保存Token**（只显示一次！）

### 第2步: 创建仓库 (30秒)
1. 访问：https://github.com/new
2. 仓库名：`awsome_reward`
3. 设为 **Public**
4. 点击 "Create repository"

### 第3步: 推送代码 (1分钟)
```bash
./github_token_push.sh
```
按提示输入：
- GitHub用户名：`serenhiworld`
- 仓库名：`awsome_reward`  
- Personal Access Token：(您刚才复制的token)

### 第4步: 启用Pages (30秒)
推送成功后：
1. 进入仓库 Settings → Pages
2. Source选择 "Deploy from a branch"
3. Branch选择 "main"
4. 点击 Save

## 🎉 完成！

✅ **网站地址**：https://serenhiworld.github.io/awsome_reward  
✅ **仓库地址**：https://github.com/serenhiworld/awsome_reward  
✅ **自动部署**：每次推送代码自动更新网站  

## 🔧 备用方案

如果脚本遇到问题，手动推送：
```bash
git remote add origin https://YOUR_TOKEN@github.com/serenhiworld/awsome_reward.git
git push -u origin main
```
将 `YOUR_TOKEN` 替换为您的实际token。

---

💡 **遇到问题？** 查看详细指南：`GOOGLE_GITHUB_GUIDE.md`
