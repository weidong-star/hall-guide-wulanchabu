#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成政务服务大厅H5导览页面模板
包含响应式设计、语音播报、事项展示等功能
"""

import argparse
import os


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{hall_name} - 政务服务大厅导览</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- 顶部导航 -->
        <header class="header">
            <div class="header-content">
                <h1 class="hall-name" id="hallName">政务服务大厅</h1>
                <button class="voice-btn" id="voiceBtn" title="语音播报">
                    <span class="icon">🔊</span>
                </button>
            </div>
        </header>

        <!-- 大厅基本信息 -->
        <section class="hall-info" id="hallInfo">
            <div class="info-card">
                <img class="hall-image" id="hallImage" src="" alt="大厅实景" onerror="this.style.display='none'">
                <div class="info-content">
                    <div class="info-item">
                        <span class="label">📍 地址：</span>
                        <span class="value" id="address">-</span>
                    </div>
                    <div class="info-item">
                        <span class="label">📞 电话：</span>
                        <span class="value" id="phone">-</span>
                    </div>
                    <div class="info-item">
                        <span class="label">🕐 办公时间：</span>
                        <span class="value" id="workTime">-</span>
                    </div>
                    <div class="info-item">
                        <span class="label">🏢 入驻单位：</span>
                        <span class="value" id="units">-</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- 温馨提示 -->
        <section class="notice" id="notice" style="display: none;">
            <div class="notice-content">
                <span class="notice-icon">📢</span>
                <span class="notice-text" id="noticeText"></span>
            </div>
        </section>

        <!-- 窗口信息 -->
        <section class="section">
            <h2 class="section-title">🪟 办事窗口</h2>
            <div class="windows-list" id="windowsList">
                <!-- 窗口列表动态生成 -->
            </div>
        </section>

        <!-- 事项清单 -->
        <section class="section">
            <h2 class="section-title">📋 办事事项</h2>
            <div class="items-list" id="itemsList">
                <!-- 事项列表动态生成 -->
            </div>
        </section>

        <!-- 底部 -->
        <footer class="footer">
            <p>如有疑问，请咨询大厅服务台</p>
        </footer>
    </div>

    <script src="app.js"></script>
</body>
</html>
"""

CSS_TEMPLATE = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    background: #f5f5f5;
    line-height: 1.6;
    color: #333;
}

.container {
    max-width: 750px;
    margin: 0 auto;
    background: #fff;
    min-height: 100vh;
}

/* 顶部导航 */
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    padding: 20px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.hall-name {
    font-size: 20px;
    font-weight: 600;
    flex: 1;
}

.voice-btn {
    background: rgba(255,255,255,0.2);
    border: none;
    color: #fff;
    padding: 10px 15px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 18px;
    transition: all 0.3s;
}

.voice-btn:hover {
    background: rgba(255,255,255,0.3);
}

.voice-btn.playing {
    background: rgba(255,255,255,0.4);
    animation: pulse 1s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}

/* 大厅基本信息 */
.hall-info {
    padding: 20px;
}

.info-card {
    background: #fff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.hall-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    display: block;
}

.info-content {
    padding: 15px;
}

.info-item {
    padding: 8px 0;
    display: flex;
    align-items: flex-start;
    border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
    border-bottom: none;
}

.label {
    font-weight: 500;
    min-width: 90px;
    flex-shrink: 0;
}

.value {
    flex: 1;
    color: #666;
}

/* 温馨提示 */
.notice {
    margin: 15px 20px;
    background: #fff3e0;
    border-left: 4px solid #ff9800;
    border-radius: 4px;
    padding: 12px 15px;
}

.notice-content {
    display: flex;
    align-items: center;
}

.notice-icon {
    font-size: 20px;
    margin-right: 10px;
}

.notice-text {
    flex: 1;
    color: #e65100;
    font-size: 14px;
}

/* 区块标题 */
.section {
    margin: 20px;
}

.section-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 15px;
    padding-left: 10px;
    border-left: 4px solid #667eea;
}

/* 窗口列表 */
.windows-list {
    display: grid;
    gap: 12px;
}

.window-card {
    background: #f9f9f9;
    border-radius: 8px;
    padding: 15px;
    border-left: 3px solid #667eea;
}

.window-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.window-name {
    font-weight: 600;
    font-size: 16px;
}

.window-services {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 8px;
}

.service-tag {
    background: #e3f2fd;
    color: #1976d2;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
}

.window-desc {
    color: #666;
    font-size: 14px;
}

/* 事项列表 */
.items-list {
    display: grid;
    gap: 12px;
}

.item-card {
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 15px;
}

.item-name {
    font-weight: 600;
    font-size: 16px;
    margin-bottom: 10px;
    color: #333;
}

.item-detail {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-bottom: 10px;
}

.item-detail-row {
    display: flex;
    align-items: center;
    font-size: 14px;
}

.item-detail-label {
    color: #666;
    margin-right: 5px;
    min-width: 50px;
}

.item-detail-value {
    color: #333;
    font-weight: 500;
}

.item-process {
    background: #f5f5f5;
    padding: 10px;
    border-radius: 4px;
    font-size: 14px;
    color: #666;
}

/* 底部 */
.footer {
    text-align: center;
    padding: 20px;
    color: #999;
    font-size: 14px;
    margin-top: 20px;
}
"""

JS_TEMPLATE = """// 获取大厅ID
function getHallId() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id') || '001';
}

// 加载大厅数据
async function loadHallData(hallId) {
    try {
        const response = await fetch(`data/hall_${hallId}.json`);
        if (!response.ok) {
            throw new Error('数据加载失败');
        }
        const data = await response.json();
        renderHall(data);
        return data;
    } catch (error) {
        console.error('加载失败:', error);
        document.getElementById('hallName').textContent = '数据加载失败，请稍后重试';
        return null;
    }
}

// 渲染大厅信息
function renderHall(data) {
    // 基本信息
    document.getElementById('hallName').textContent = data.hallName;
    document.getElementById('address').textContent = data.address || '-';
    document.getElementById('phone').textContent = data.phone || '-';
    document.getElementById('workTime').textContent = data.workTime || '-';
    document.getElementById('units').textContent = data.units ? `${data.units}家` : '-';

    // 大厅图片
    if (data.image) {
        document.getElementById('hallImage').src = data.image;
    }

    // 温馨提示
    if (data.notice) {
        document.getElementById('notice').style.display = 'block';
        document.getElementById('noticeText').textContent = data.notice;
    }

    // 渲染窗口列表
    if (data.windows && data.windows.length > 0) {
        const windowsList = document.getElementById('windowsList');
        windowsList.innerHTML = data.windows.map(window => `
            <div class="window-card">
                <div class="window-header">
                    <span class="window-name">${window.name}</span>
                </div>
                ${window.services && window.services.length > 0 ? `
                    <div class="window-services">
                        ${window.services.map(service => `<span class="service-tag">${service}</span>`).join('')}
                    </div>
                ` : ''}
                ${window.description ? `<div class="window-desc">${window.description}</div>` : ''}
            </div>
        `).join('');
    }

    // 渲染事项列表
    if (data.items && data.items.length > 0) {
        const itemsList = document.getElementById('itemsList');
        itemsList.innerHTML = data.items.map(item => `
            <div class="item-card">
                <div class="item-name">${item.name}</div>
                ${item.materials || item.time || item.fee ? `
                    <div class="item-detail">
                        ${item.materials ? `
                            <div class="item-detail-row">
                                <span class="item-detail-label">材料：</span>
                                <span class="item-detail-value">${item.materials.join('、')}</span>
                            </div>
                        ` : ''}
                        ${item.time ? `
                            <div class="item-detail-row">
                                <span class="item-detail-label">时限：</span>
                                <span class="item-detail-value">${item.time}</span>
                            </div>
                        ` : ''}
                        ${item.fee ? `
                            <div class="item-detail-row">
                                <span class="item-detail-label">费用：</span>
                                <span class="item-detail-value">${item.fee}</span>
                            </div>
                        ` : ''}
                    </div>
                ` : ''}
                ${item.process ? `
                    <div class="item-process">
                        <strong>办理流程：</strong>${item.process}
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    // 保存语音文本用于播报
    document.getElementById('voiceBtn').dataset.voiceText = data.voiceText || '';
}

// 语音播报
let isPlaying = false;
function playVoice(text) {
    if (!text) {
        alert('暂无语音介绍');
        return;
    }

    if (isPlaying) {
        speechSynthesis.cancel();
        isPlaying = false;
        document.getElementById('voiceBtn').classList.remove('playing');
        return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    utterance.rate = 1.0;

    utterance.onend = () => {
        isPlaying = false;
        document.getElementById('voiceBtn').classList.remove('playing');
    };

    utterance.onerror = () => {
        isPlaying = false;
        document.getElementById('voiceBtn').classList.remove('playing');
        alert('语音播放失败');
    };

    speechSynthesis.speak(utterance);
    isPlaying = true;
    document.getElementById('voiceBtn').classList.add('playing');
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    const hallId = getHallId();
    loadHallData(hallId).then(data => {
        if (data && data.voiceText) {
            document.getElementById('voiceBtn').addEventListener('click', () => {
                playVoice(data.voiceText);
            });
        } else {
            document.getElementById('voiceBtn').style.display = 'none';
        }
    });
});
"""


def main():
    parser = argparse.ArgumentParser(description='生成政务服务大厅H5导览页面模板')
    parser.add_argument('--domain', type=str, default='https://example.com',
                       help='部署域名（用于生成二维码URL，默认 https://example.com）')
    parser.add_argument('--output-dir', type=str, default='.',
                       help='输出目录（默认当前目录）')

    args = parser.parse_args()

    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)

    # 生成文件
    files = {
        'hall.html': HTML_TEMPLATE.format(hall_name="政务服务大厅"),
        'style.css': CSS_TEMPLATE,
        'app.js': JS_TEMPLATE
    }

    for filename, content in files.items():
        output_path = os.path.join(args.output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 已生成：{filename}")

    # 创建 data 目录
    data_dir = os.path.join(args.output_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    print(f"✅ 已创建目录：data/")

    # 创建 images 目录
    images_dir = os.path.join(args.output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    print(f"✅ 已创建目录：images/")

    print("\n📋 生成完成！")
    print("\n下一步：")
    print("1. 运行脚本生成数据结构模板：")
    print("   python scripts/generate-data-structure.py --hall-count 12")
    print("2. 编辑数据模板，填写实际信息")
    print("3. 将数据文件放入 data/ 目录，命名为 hall_001.json, hall_002.json, ...")
    print("4. 将大厅照片放入 images/ 目录，命名为 hall_001.jpg, hall_002.jpg, ...")
    print("5. 部署到 GitHub Pages 或 Vercel")
    print(f"6. 访问示例：{args.domain}/hall.html?id=001")


if __name__ == "__main__":
    main()
