#!/bin/bash

echo "🚀 GitHub部署助手"
echo "================="

# 检查Git是否已安装
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装，请先安装Git"
    exit 1
fi

echo "📋 请按提示输入信息:"
echo ""

# 获取GitHub用户名
read -p "🔸 请输入您的GitHub用户名: " GITHUB_USERNAME
if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub用户名不能为空"
    exit 1
fi

# 获取仓库名称
read -p "🔸 请输入仓库名称 [uk-deals-referral]: " REPO_NAME
REPO_NAME=${REPO_NAME:-uk-deals-referral}

# 获取用户邮箱
read -p "🔸 请输入您的邮箱地址: " USER_EMAIL
if [ -z "$USER_EMAIL" ]; then
    echo "❌ 邮箱地址不能为空"
    exit 1
fi

echo ""
echo "📝 配置信息:"
echo "   GitHub用户名: $GITHUB_USERNAME"
echo "   仓库名称: $REPO_NAME"
echo "   邮箱地址: $USER_EMAIL"
echo ""

read -p "是否继续部署? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "❌ 部署已取消"
    exit 1
fi

echo ""
echo "🔧 开始配置..."

# 更新README中的链接
sed -i.bak "s/your-username/$GITHUB_USERNAME/g" README.md
sed -i.bak "s/uk-deals-referral/$REPO_NAME/g" README.md

# 更新sitemap中的链接
sed -i.bak "s/your-username/$GITHUB_USERNAME/g" sitemap.xml
sed -i.bak "s/uk-deals-referral/$REPO_NAME/g" sitemap.xml

# 更新robots.txt中的链接
sed -i.bak "s/your-username/$GITHUB_USERNAME/g" robots.txt
sed -i.bak "s/uk-deals-referral/$REPO_NAME/g" robots.txt

# 配置Git用户信息
git config user.name "$GITHUB_USERNAME"
git config user.email "$USER_EMAIL"

echo "✅ 配置完成"
echo ""

# 检查是否有未提交的更改
if ! git diff --staged --quiet || ! git diff --quiet; then
    echo "📝 提交更改..."
    git add .
    git commit -m "Update: Configure GitHub username and repository name"
fi

echo "🔗 请按照以下步骤完成部署:"
echo ""
echo "1. 在GitHub上创建新仓库:"
echo "   📍 访问: https://github.com/new"
echo "   📍 仓库名称: $REPO_NAME"
echo "   📍 描述: 英国优惠推荐码分享网站 - 互惠共赢的透明推荐平台"
echo "   📍 设置为 Public"
echo "   📍 不要勾选 'Initialize this repository with a README'"
echo ""

echo "2. 推送代码到GitHub:"
echo "   git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""

echo "3. 配置GitHub Pages:"
echo "   📍 进入仓库设置页面: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings"
echo "   📍 点击左侧的 'Pages'"
echo "   📍 Source 选择 'Deploy from a branch'"
echo "   📍 Branch 选择 'main' / (root)"
echo "   📍 点击 'Save'"
echo ""

echo "4. 网站地址:"
echo "   🌐 https://$GITHUB_USERNAME.github.io/$REPO_NAME"
echo ""

read -p "是否现在推送到GitHub? (需要先在GitHub创建仓库) (y/n): " PUSH_NOW
if [ "$PUSH_NOW" = "y" ]; then
    echo "📤 推送到GitHub..."
    
    git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git
    git branch -M main
    
    if git push -u origin main; then
        echo ""
        echo "🎉 代码推送成功!"
        echo "🌐 请访问 https://github.com/$GITHUB_USERNAME/$REPO_NAME 查看仓库"
        echo "⚡ GitHub Pages将在几分钟内完成部署"
        echo "🎯 网站地址: https://$GITHUB_USERNAME.github.io/$REPO_NAME"
    else
        echo ""
        echo "❌ 推送失败，请检查:"
        echo "   1. 是否已在GitHub创建仓库"
        echo "   2. 是否有正确的访问权限"
        echo "   3. 网络连接是否正常"
    fi
else
    echo ""
    echo "📋 手动推送命令:"
    echo "git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo "git branch -M main"
    echo "git push -u origin main"
fi

echo ""
echo "📚 更多帮助:"
echo "   📖 部署指南: DEPLOY_GUIDE.md"
echo "   🤖 爬虫指南: CRAWLER_GUIDE.md"
echo "   📊 项目总结: PROJECT_SUMMARY.md"
echo ""
echo "🎊 部署完成！祝您推荐码分享成功！"
