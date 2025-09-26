#!/bin/bash

echo "🚀 英国优惠爬虫启动脚本"
echo "=========================="

# 检查Python版本
python_version=$(python3 --version 2>&1)
echo "Python版本: $python_version"

# 创建必要的目录
echo "创建目录结构..."
mkdir -p data
mkdir -p logs
mkdir -p backups

# 检查并安装依赖
echo "检查Python依赖..."
if [ -f "requirements.txt" ]; then
    echo "安装依赖包..."
    pip3 install -r requirements.txt
else
    echo "⚠️  requirements.txt 文件不存在"
fi

# 检查配置文件
if [ ! -f "config.py" ]; then
    echo "⚠️  配置文件 config.py 不存在"
fi

# 选择运行模式
echo ""
echo "请选择运行模式:"
echo "1. 立即运行一次爬虫"
echo "2. 启动定时调度器(后台运行)"
echo "3. 测试爬虫功能"
echo "4. 查看日志"
echo "5. 停止后台服务"

read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo "🔄 立即运行爬虫..."
        python3 crawler.py
        ;;
    2)
        echo "⏰ 启动定时调度器..."
        nohup python3 scheduler.py > logs/scheduler.log 2>&1 &
        echo "定时调度器已启动，进程ID: $!"
        echo "可以使用 'ps aux | grep scheduler.py' 查看进程状态"
        echo "日志文件: logs/scheduler.log"
        ;;
    3)
        echo "🧪 测试爬虫功能..."
        python3 -c "
from crawler import LatestFreeStuffCrawler
import json

crawler = LatestFreeStuffCrawler()
print('测试网站连接...')
content = crawler.get_page_content('https://www.latestfreestuff.co.uk')
if content:
    print('✅ 网站连接成功')
    deals = crawler.parse_deals(content)
    print(f'✅ 找到 {len(deals)} 个优惠信息')
    if deals:
        print('第一个优惠信息:')
        print(json.dumps(deals[0], indent=2, ensure_ascii=False))
else:
    print('❌ 网站连接失败')
"
        ;;
    4)
        echo "📝 查看最新日志..."
        if [ -f "crawler.log" ]; then
            tail -50 crawler.log
        else
            echo "日志文件不存在"
        fi
        ;;
    5)
        echo "⏹️  停止后台服务..."
        pkill -f "python3 scheduler.py"
        echo "后台服务已停止"
        ;;
    *)
        echo "❌ 无效选项"
        ;;
esac

echo ""
echo "脚本执行完毕"
