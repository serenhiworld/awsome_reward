#!/bin/bash

echo "🚀 GitHub推送和部署脚本"
echo "=========================="

# 检查是否在正确的目录
if [ ! -f "index.html" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

# 获取用户输入
echo "📝 请输入GitHub相关信息:"
read -p "GitHub用户名: " github_username
read -p "仓库名称 (建议: uk-referral-deals): " repo_name

# 设置默认仓库名
if [ -z "$repo_name" ]; then
    repo_name="uk-referral-deals"
fi

echo ""
echo "📋 配置信息确认:"
echo "用户名: $github_username"
echo "仓库名: $repo_name"
echo "仓库地址: https://github.com/$github_username/$repo_name"
echo ""

read -p "信息正确吗？(y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "已取消操作"
    exit 1
fi

echo ""
echo "🔧 更新配置文件..."

# 更新robots.txt中的网站地址
sed -i "s/your-username/$github_username/g" robots.txt
sed -i "s/uk-deals-referral/$repo_name/g" robots.txt

# 更新sitemap.xml中的网站地址
sed -i "s/your-username/$github_username/g" sitemap.xml
sed -i "s/uk-deals-referral/$repo_name/g" sitemap.xml

echo "✅ 配置文件已更新"

echo ""
echo "📦 添加所有文件到Git..."
git add .

echo "💾 提交更改..."
git commit -m "Update GitHub Pages configuration

- Update robots.txt with correct repository URL
- Update sitemap.xml with correct repository URL
- Ready for GitHub Pages deployment"

echo ""
echo "🔗 设置远程仓库地址..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/$github_username/$repo_name.git

echo ""
echo "📤 推送到GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 推送成功！"
    echo ""
    echo "📋 下一步操作:"
    echo "1. 访问: https://github.com/$github_username/$repo_name"
    echo "2. 进入 Settings > Pages"
    echo "3. 选择 'Deploy from a branch'"
    echo "4. 选择 'main' 分支和 '/ (root)' 文件夹"
    echo "5. 点击 Save"
    echo ""
    echo "🌐 部署完成后网站地址:"
    echo "https://$github_username.github.io/$repo_name/"
    echo ""
    echo "⏰ 部署通常需要2-5分钟时间"
else
    echo ""
    echo "❌ 推送失败，可能的原因:"
    echo "1. 仓库不存在，请先在GitHub创建仓库"
    echo "2. 没有推送权限"
    echo "3. 网络连接问题"
    echo ""
    echo "请检查后重试"
fi
