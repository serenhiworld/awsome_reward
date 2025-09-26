# 🚀 serenhiworld账户GitHub部署指南

## 🎯 当前配置

- **GitHub用户名**: serenhiworld
- **仓库名**: awsome_reward
- **网站地址**: https://serenhiworld.github.io/awsome_reward

## 🔧 权限问题解决方案

### 方法一：使用个人访问令牌（推荐）

1. **创建个人访问令牌**:
   - 访问: https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 勾选 `repo` 权限
   - 点击 "Generate token"
   - **复制生成的令牌**（只显示一次）

2. **使用令牌推送**:
   ```bash
   git remote set-url origin https://serenhiworld:YOUR_TOKEN@github.com/serenhiworld/awsome_reward.git
   git push -u origin main
   ```

### 方法二：使用SSH密钥

1. **生成SSH密钥**:
   ```bash
   ssh-keygen -t ed25519 -C "serenhiworld@gmail.com"
   ```

2. **添加SSH密钥到GitHub**:
   - 复制公钥: `cat ~/.ssh/id_ed25519.pub`
   - 访问: https://github.com/settings/ssh
   - 点击 "New SSH key"
   - 粘贴公钥内容

3. **使用SSH推送**:
   ```bash
   git remote set-url origin git@github.com:serenhiworld/awsome_reward.git
   git push -u origin main
   ```

### 方法三：GitHub CLI

1. **安装GitHub CLI**:
   ```bash
   sudo apt update
   sudo apt install gh
   ```

2. **登录并推送**:
   ```bash
   gh auth login
   git push -u origin main
   ```

## 📋 完整部署步骤

### 1. 确保GitHub仓库存在
访问 https://github.com/new 创建新仓库:
- 仓库名: `awsome_reward`
- 设置为 Public
- 不要勾选 "Initialize with README"

### 2. 运行专用推送脚本
```bash
./push_to_serenhiworld.sh
```

### 3. 配置GitHub Pages
1. 访问: https://github.com/serenhiworld/awsome_reward/settings/pages
2. Source: Deploy from a branch
3. Branch: main / (root)
4. 点击 Save

### 4. 访问网站
等待几分钟后访问: https://serenhiworld.github.io/awsome_reward

## 🔍 故障排除

### 403权限错误
- 确保使用正确的用户名和密码/令牌
- 检查仓库是否存在
- 确认有推送权限

### 仓库不存在
- 在GitHub手动创建仓库
- 确保仓库名正确: `awsome_reward`

### 网络问题
- 检查网络连接
- 尝试使用VPN
- 使用SSH替代HTTPS

## 🎉 成功后的步骤

1. ✅ 网站上线: https://serenhiworld.github.io/awsome_reward
2. ✅ 开始分享推荐码
3. ✅ 定期更新内容
4. ✅ 监控网站流量

---

💡 **提示**: 推送成功后，GitHub Actions会自动部署网站，无需手动操作！
