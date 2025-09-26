#!/bin/bash

echo "🚀 GitHub简化部署方案"
echo "===================="

echo "由于GitHub已停止支持密码认证，这里提供几种简单的替代方案："
echo ""

echo "📋 方案一：使用GitHub Desktop（推荐新手）"
echo "1. 下载安装 GitHub Desktop: https://desktop.github.com/"
echo "2. 登录您的GitHub账号"
echo "3. 点击 'Add' → 'Add existing repository'"
echo "4. 选择项目文件夹: $(pwd)"
echo "5. 点击 'Publish repository' 发布到GitHub"
echo ""

echo "📋 方案二：使用Personal Access Token"
echo "1. 访问: https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 勾选 'repo' 权限"
echo "4. 复制生成的token"
echo "5. 运行以下命令:"
echo "   git remote add origin https://github.com/serenhiworld/awsome_reward.git"
echo "   git push -u origin main"
echo "   # 用户名输入: serenhiworld"
echo "   # 密码输入: [粘贴刚才的token]"
echo ""

echo "📋 方案三：使用GitHub CLI"
echo "1. 安装 GitHub CLI: https://cli.github.com/"
echo "2. 运行: gh auth login"
echo "3. 运行: gh repo create awsome_reward --public --source=."
echo "4. 运行: git push -u origin main"
echo ""

echo "📋 方案四：手动上传（最简单）"
echo "1. 访问 https://github.com/new 创建新仓库"
echo "2. 仓库名: awsome_reward"
echo "3. 设置为 Public"
echo "4. 点击 'uploading an existing file'"
echo "5. 将所有文件拖拽上传"
echo ""

echo "✅ 推荐使用方案一（GitHub Desktop），最简单易用！"

# 创建一个压缩包方便上传
echo ""
echo "🗜️ 正在创建项目压缩包..."
tar -czf awsome_reward_$(date +%Y%m%d).tar.gz \
    --exclude='.git' \
    --exclude='crawler/data' \
    --exclude='*.log' \
    --exclude='*backup*' \
    .

if [ -f "awsome_reward_$(date +%Y%m%d).tar.gz" ]; then
    echo "✅ 压缩包已创建: awsome_reward_$(date +%Y%m%d).tar.gz"
    echo "💡 您可以下载这个压缩包，解压后手动上传到GitHub"
else
    echo "❌ 压缩包创建失败"
fi
