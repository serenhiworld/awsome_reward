#!/bin/bash

echo "🔑 GitHub Personal Access Token 一键设置"
echo "========================================"
echo ""
echo "GitHub已不再支持密码认证，需要使用Personal Access Token"
echo ""

echo "📝 第一步：创建Personal Access Token"
echo "1. 访问: https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 填写描述: awsome_reward_deploy"
echo "4. 勾选权限: repo (完整仓库权限)"
echo "5. 点击 'Generate token'"
echo "6. 复制生成的token（类似：ghp_xxxxxxxxxxxx）"
echo ""

read -p "已创建token？请粘贴您的Personal Access Token: " token

if [ -z "$token" ]; then
    echo "❌ Token不能为空"
    exit 1
fi

echo ""
echo "🔧 配置Git..."

# 配置Git用户信息
git config user.name "serenhiworld"
git config user.email "serenhiworld@gmail.com"

# 添加远程仓库（不包含密码）
git remote add origin https://github.com/serenhiworld/awsome_reward.git

echo ""
echo "📤 推送到GitHub..."

# 使用token进行推送
if git push https://serenhiworld:$token@github.com/serenhiworld/awsome_reward.git main; then
    echo ""
    echo "🎉 推送成功！"
    echo ""
    echo "📋 下一步：配置GitHub Pages"
    echo "1. 访问: https://github.com/serenhiworld/awsome_reward"
    echo "2. 点击 'Settings' 标签"
    echo "3. 在左侧菜单点击 'Pages'"
    echo "4. 在 'Source' 下选择 'Deploy from a branch'"
    echo "5. 选择 'main' 分支，'/ (root)' 文件夹"
    echo "6. 点击 'Save'"
    echo ""
    echo "🌐 您的网站将在几分钟内部署到:"
    echo "https://serenhiworld.github.io/awsome_reward"
    echo ""
    echo "✅ 部署完成！"
else
    echo ""
    echo "❌ 推送失败，可能的原因:"
    echo "1. Token权限不够（需要repo权限）"
    echo "2. 仓库不存在（请先在GitHub创建）"
    echo "3. Token已过期"
    echo ""
    echo "💡 解决方案:"
    echo "- 访问 https://github.com/new 创建仓库名为 'awsome_reward'"
    echo "- 确保仓库设置为 Public"
    echo "- 重新生成token并确保有repo权限"
fi

# 清理敏感信息
unset token
echo ""
echo "🔒 已清理敏感信息"
