#!/bin/bash

echo "🔐 GitHub Token推送脚本 (适用于Google登录账户)"
echo "================================================"

# 检查是否在正确的目录
if [ ! -f "index.html" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

echo ""
echo "📝 使用Google账号登录的GitHub需要Personal Access Token"
echo "如果您还没有创建Token，请先访问："
echo "👉 https://github.com/settings/tokens"
echo ""

# 获取用户信息
read -p "🔸 GitHub用户名 [serenhiworld]: " github_username
github_username=${github_username:-serenhiworld}

read -p "🔸 仓库名称 [awsome_reward]: " repo_name
repo_name=${repo_name:-awsome_reward}

echo ""
echo "🔑 请输入您的Personal Access Token:"
echo "   (Token格式: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)"
read -s -p "Token: " github_token
echo ""

# 验证输入
if [ -z "$github_token" ]; then
    echo "❌ Token不能为空"
    exit 1
fi

if [[ ! $github_token =~ ^ghp_ ]]; then
    echo "⚠️  警告: Token格式可能不正确（通常以ghp_开头）"
    read -p "是否继续? (y/n): " continue_anyway
    if [ "$continue_anyway" != "y" ]; then
        echo "❌ 操作已取消"
        exit 1
    fi
fi

echo ""
echo "📋 配置确认:"
echo "   GitHub用户: $github_username"
echo "   仓库名称: $repo_name"
echo "   Token: ${github_token:0:7}***"
echo ""

read -p "信息正确吗? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ 操作已取消"
    exit 1
fi

echo ""
echo "🔧 开始推送..."

# 配置Git用户信息
echo "⚙️  配置Git用户信息..."
git config user.name "$github_username"
git config user.email "${github_username}@users.noreply.github.com"

# 删除旧的远程配置
echo "🗑️  清理旧配置..."
git remote remove origin 2>/dev/null || true

# 添加新的远程仓库
echo "🔗 设置远程仓库..."
git remote add origin "https://${github_token}@github.com/${github_username}/${repo_name}.git"

# 检查是否有未提交的更改
if ! git diff --staged --quiet || ! git diff --quiet; then
    echo "📝 提交最新更改..."
    git add .
    git commit -m "Update: Ready for GitHub Pages deployment with Google account authentication"
fi

# 推送到GitHub
echo "📤 推送代码到GitHub..."
if git push -u origin main; then
    echo ""
    echo "🎉 推送成功！"
    echo ""
    echo "📋 下一步操作:"
    echo "1. 访问仓库: https://github.com/$github_username/$repo_name"
    echo "2. 进入 Settings → Pages"
    echo "3. Source 选择 'Deploy from a branch'"
    echo "4. Branch 选择 'main'"
    echo "5. 点击 Save"
    echo ""
    echo "⏱️  GitHub Pages通常需要2-5分钟部署完成"
    echo "🌐 网站地址: https://$github_username.github.io/$repo_name"
    echo ""
    echo "🔒 安全提示: 请妥善保管您的Personal Access Token"
    
else
    echo ""
    echo "❌ 推送失败，可能的原因:"
    echo "1. Token权限不足（确保勾选了repo权限）"
    echo "2. Token已过期或无效"
    echo "3. 仓库不存在（请先在GitHub创建仓库）"
    echo "4. 网络连接问题"
    echo ""
    echo "💡 解决建议:"
    echo "- 检查Token权限和有效性"
    echo "- 确保在GitHub上创建了名为 '$repo_name' 的仓库"
    echo "- 确保仓库设置为Public（免费账户的Pages要求）"
    
    exit 1
fi

# 清理敏感信息
echo "🧹 清理认证信息..."
git remote set-url origin "https://github.com/$github_username/$repo_name.git"

echo ""
echo "✅ 部署脚本完成！"
