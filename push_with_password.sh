#!/bin/bash

echo "🚀 GitHub账号密码推送脚本"
echo "============================"

# 检查是否在项目目录
if [ ! -f "index.html" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

echo "📝 请输入GitHub登录信息:"
read -p "GitHub用户名: " github_username
read -s -p "GitHub密码: " github_password
echo ""

# 验证输入
if [ -z "$github_username" ] || [ -z "$github_password" ]; then
    echo "❌ 用户名和密码不能为空"
    exit 1
fi

echo ""
echo "🔧 配置Git用户信息..."
git config user.name "$github_username"
git config user.email "${github_username}@users.noreply.github.com"

echo "🔗 检查远程仓库配置..."
current_remote=$(git remote get-url origin 2>/dev/null || echo "")

if [ -z "$current_remote" ]; then
    echo "📋 需要添加远程仓库地址"
    read -p "请输入仓库名称 (默认: awsome_reward): " repo_name
    repo_name=${repo_name:-awsome_reward}
    
    echo "🔗 添加远程仓库..."
    git remote add origin https://${github_username}:${github_password}@github.com/${github_username}/${repo_name}.git
else
    echo "🔄 更新远程仓库认证信息..."
    # 移除旧的远程地址
    git remote remove origin
    
    # 从当前远程URL提取仓库名
    repo_name=$(echo "$current_remote" | sed 's/.*\/\([^/]*\)\.git$/\1/')
    
    # 添加带认证信息的新远程地址
    git remote add origin https://${github_username}:${github_password}@github.com/${github_username}/${repo_name}.git
fi

echo "📤 推送代码到GitHub..."
if git push -u origin main; then
    echo ""
    echo "🎉 推送成功！"
    echo "🌐 仓库地址: https://github.com/${github_username}/${repo_name}"
    echo ""
    echo "📋 下一步配置GitHub Pages:"
    echo "1. 访问: https://github.com/${github_username}/${repo_name}/settings/pages"
    echo "2. Source选择: Deploy from a branch"
    echo "3. Branch选择: main"
    echo "4. 点击Save"
    echo ""
    echo "⚡ 几分钟后您的网站将在以下地址可访问:"
    echo "🎯 https://${github_username}.github.io/${repo_name}"
else
    echo ""
    echo "❌ 推送失败，可能的原因:"
    echo "1. 用户名或密码错误"
    echo "2. 仓库不存在，请先在GitHub创建仓库"
    echo "3. 网络连接问题"
    echo ""
    echo "💡 解决方案:"
    echo "- 检查GitHub登录信息是否正确"
    echo "- 在GitHub上创建名为 '${repo_name}' 的仓库"
    echo "- 确保仓库设置为Public（免费账户的私有仓库无法使用Pages）"
fi

# 清理敏感信息
unset github_password

echo ""
echo "🔒 安全提示: 脚本已清理密码信息"
