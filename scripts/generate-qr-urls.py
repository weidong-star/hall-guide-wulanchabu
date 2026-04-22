#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成政务服务大厅二维码URL列表
用于生成二维码贴纸
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description='生成政务服务大厅二维码URL列表')
    parser.add_argument('--domain', type=str, required=True,
                       help='部署域名（必填，如 https://example.com）')
    parser.add_argument('--hall-count', type=int, default=12,
                       help='大厅数量（默认12）')
    parser.add_argument('--output', type=str, default='qr-urls.txt',
                       help='输出文件名（默认qr-urls.txt）')

    args = parser.parse_args()

    # 确保域名格式正确
    domain = args.domain.rstrip('/')
    if not domain.startswith('http://') and not domain.startswith('https://'):
        domain = 'https://' + domain

    # 生成二维码URL列表
    lines = []
    lines.append("=" * 60)
    lines.append("政务服务大厅二维码URL列表")
    lines.append("=" * 60)
    lines.append(f"域名: {domain}")
    lines.append(f"大厅数量: {args.hall_count}")
    lines.append("=" * 60)
    lines.append("")

    for i in range(1, args.hall_count + 1):
        hall_id = str(i).zfill(3)
        url = f"{domain}/hall.html?id={hall_id}"
        lines.append(f"大厅 {hall_id}: {url}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("使用说明：")
    lines.append("=" * 60)
    lines.append("1. 复制每个大厅的URL到草料二维码（https://cli.im）生成二维码")
    lines.append("2. 下载生成的二维码图片")
    lines.append("3. 将二维码贴在对应大厅的入口处")
    lines.append("4. 用户扫码即可查看大厅详细信息")
    lines.append("")

    # 写入文件
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"✅ 二维码URL列表已生成：{args.output}")
    print(f"✅ 共生成 {args.hall_count} 个大厅的二维码URL")
    print("\n下一步：")
    print("1. 打开 qr-urls.txt 文件")
    print("2. 复制每个大厅的URL")
    print("3. 使用草料二维码（https://cli.im）生成二维码图片")
    print("4. 下载二维码并打印贴在对应大厅")


if __name__ == "__main__":
    main()
