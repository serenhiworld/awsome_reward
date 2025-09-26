#!/bin/bash

echo "🚀 GitHub推送脚本 - serenhiworld账户"
echo "====================================="

# 检查必要文件
if [ ! -f "index.html" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

echo "👤 GitHub账户信息:"
echo "用户名: serenhiworld"
echo "仓库名: awsome_reward"
echo "仓库地址: https://github.com/serenhiworld/awsome_reward"
echo ""

# 确认信息
read -p "是否使用以上信息推送代码? (y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ 操作已取消"
    exit 1
fi

echo ""
echo "📝 配置Git用户信息..."
git config user.name "serenhiworld"
git config user.email "serenhiworld@gmail.com"

echo "✅ Git配置完成"

# 检查GitHub仓库是否存在
echo ""
echo "🔍 检查GitHub仓库状态..."
if curl -s -o /dev/null -w "%{http_code}" https://github.com/serenhiworld/awsome_reward | grep -q "200"; then
    echo "✅ GitHub仓库存在"
else
    echo "⚠️  GitHub仓库可能不存在或无法访问"
    echo "请确保:"
    echo "1. 仓库已在GitHub创建: https://github.com/new"
    echo "2. 仓库名称: awsome_reward"
    echo "3. 设置为Public"
    echo ""
    read -p "仓库已创建，继续推送? (y/n): " continue_push
    if [ "$continue_push" != "y" ]; then
        echo "❌ 推送已取消"
        exit 1
    fi
fi

echo ""
echo "🔗 设置远程仓库..."
git remote add origin https://github.com/serenhiworld/awsome_reward.git

echo "📤 推送代码到GitHub..."
echo "📋 如果需要输入凭据，请使用以下信息:"
echo "   用户名: serenhiworld"
echo "   密码: 您的GitHub个人访问令牌 (不是登录密码)"
echo ""

# 推送代码
if git push -u origin main; then
    echo ""
    echo "🎉 推送成功！"
    echo "🌐 仓库地址: https://github.com/serenhiworld/awsome_reward"
    echo ""
    echo "📋 下一步: 配置GitHub Pages"
    echo "1. 访问: https://github.com/serenhiworld/awsome_reward/settings/pages"
    echo "2. Source 选择: Deploy from a branch"
    echo "3. Branch 选择: main / (root)"
    echo "4. 点击 Save"
    echo ""
    echo "⏱️  GitHub Pages将在几分钟后生效"
    echo "🌐 网站地址: https://serenhiworld.github.io/awsome_reward"
    echo ""
    echo "🎊 恭喜！您的推荐码分享网站即将上线！"
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "🔧 可能的解决方案:"
    echo ""
    echo "1. 📝 创建GitHub个人访问令牌:"
    echo "   - 访问: https://github.com/settings/tokens"
    echo "   - 点击 'Generate new token (classic)'"
    echo "   - 选择适当的权限 (repo)"
    echo "   - 复制生成的令牌"
    echo ""
    echo "2. 🔐 使用令牌推送:"
    echo "   git remote set-url origin https://serenhiworld:YOUR_TOKEN@github.com/serenhiworld/awsome_reward.git"
    echo "   git push -u origin main"
    echo ""
    echo "3. 🌐 或者在GitHub网站上手动创建仓库并上传文件"
    echo ""
    echo "4. 📞 需要帮助? 查看 GITHUB_DEPLOYMENT.md 文档"
fi
