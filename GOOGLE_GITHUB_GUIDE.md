# 🔐 GitHub Google账号登录部署指南

## 📋 重要说明
您使用Google账号登录GitHub，无法使用传统的用户名/密码方式推送代码。需要使用Personal Access Token (PAT)。

## 🚀 快速部署步骤

### 步骤1: 创建Personal Access Token

1. **登录GitHub**
   - 访问 https://github.com
   - 使用Google账号登录

2. **创建Token**
   - 点击右上角头像 → Settings
   - 左侧菜单选择 "Developer settings"
   - 选择 "Personal access tokens" → "Tokens (classic)"
   - 点击 "Generate new token" → "Generate new token (classic)"

3. **配置Token**
   - **Note**: 填写 "UK Referral Website"
   - **Expiration**: 选择 "No expiration"（不过期）
   - **权限选择**:
     - ✅ `repo` (完整仓库权限)
     - ✅ `workflow` (GitHub Actions)
     - ✅ `write:packages` (包权限)
   - 点击 "Generate token"

4. **保存Token**
   - ⚠️ **重要**: 立即复制并保存Token
   - Token只会显示一次，请妥善保管
   - 格式类似: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 步骤2: 在GitHub创建仓库

1. **创建新仓库**
   - 访问 https://github.com/new
   - **Repository name**: `awsome_reward`
   - **Description**: `英国优惠推荐码分享网站 - 透明诚信的互惠共赢平台`
   - 选择 **Public**（免费GitHub Pages需要公开仓库）
   - **不要** 勾选任何初始化选项
   - 点击 "Create repository"

### 步骤3: 推送代码

使用以下命令（将YOUR_TOKEN替换为您的实际token）:

```bash
# 删除旧的远程配置
git remote remove origin 2>/dev/null || true

# 添加新的远程仓库（使用token认证）
git remote add origin https://YOUR_TOKEN@github.com/serenhiworld/awsome_reward.git

# 推送代码
git push -u origin main
```

### 步骤4: 配置GitHub Pages

1. **进入仓库设置**
   - 在您的仓库页面，点击 "Settings"
   - 左侧菜单找到 "Pages"

2. **配置Pages**
   - **Source**: 选择 "Deploy from a branch"
   - **Branch**: 选择 "main"
   - **Folder**: 选择 "/ (root)"
   - 点击 "Save"

3. **等待部署**
   - 部署通常需要2-5分钟
   - 完成后会显示网站地址: `https://serenhiworld.github.io/awsome_reward`

## 🛠️ 使用一键脚本

我为您创建了一个专门的推送脚本，运行后按提示操作：

```bash
./github_token_push.sh
```

## 🔒 安全提示

- Token具有完整的GitHub访问权限，请妥善保管
- 不要在公开场合分享Token
- 可以随时在GitHub设置中删除或重新生成Token

## ❌ 故障排除

### 问题1: Token无效
- 检查Token是否正确复制
- 确认Token权限包含repo权限
- 确认Token未过期

### 问题2: 推送被拒绝
- 确认仓库名称正确: `awsome_reward`
- 确认仓库设置为Public
- 检查网络连接

### 问题3: Pages不工作
- 确认仓库为Public
- 检查是否有index.html文件
- 等待几分钟让部署完成

## 🎉 完成后的结果

成功后您将拥有：
- ✅ GitHub仓库: `https://github.com/serenhiworld/awsome_reward`
- ✅ 在线网站: `https://serenhiworld.github.io/awsome_reward`
- ✅ 自动部署: 每次推送代码自动更新网站
- ✅ HTTPS安全连接
- ✅ 全球CDN加速

---

💡 **需要帮助？** 如遇问题可以参考详细的图文教程或联系技术支持。
