#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成政务服务大厅数据结构模板
用于创建标准化的JSON数据配置文件
"""

import argparse
import json
import os


def generate_hall_template(hall_id):
    """生成单个大厅的数据模板"""
    return {
        "hallId": hall_id,
        "hallName": f"政务服务大厅-{hall_id}",
        "address": "XX市XX区XX街道1号",
        "phone": "0471-1234567",
        "workTime": "周一至周五 9:00-17:00",
        "units": 25,
        "windows": [
            {
                "id": f"w{hall_id}001",
                "name": "公安户政窗口",
                "services": ["身份证办理", "户口迁移", "居住证申领"],
                "description": "提供户籍业务全流程服务"
            },
            {
                "id": f"w{hall_id}002",
                "name": "社保窗口",
                "services": ["社保查询", "社保转移", "退休办理"],
                "description": "提供社会保险相关业务办理"
            }
        ],
        "items": [
            {
                "id": f"i{hall_id}001",
                "name": "身份证办理",
                "materials": ["户口本", "照片"],
                "process": "取号→窗口办理→缴费→领取",
                "time": "5个工作日",
                "fee": "20元"
            }
        ],
        "voiceText": f"欢迎来到{hall_id}号政务服务大厅，现有入驻单位25家，共设窗口30个，提供公安户政、社会保障等一站式服务。",
        "notice": "温馨提示：请携带有效身份证件办理业务",
        "image": f"images/hall_{hall_id}.jpg"
    }


def main():
    parser = argparse.ArgumentParser(description='生成政务服务大厅数据结构模板')
    parser.add_argument('--hall-count', type=int, default=12,
                       help='大厅数量（默认12）')
    parser.add_argument('--output', type=str, default='hall-data-template.json',
                       help='输出文件名（默认hall-data-template.json）')

    args = parser.parse_args()

    # 生成所有大厅的数据模板
    halls = []
    for i in range(1, args.hall_count + 1):
        hall_id = str(i).zfill(3)
        halls.append(generate_hall_template(hall_id))

    # 生成完整的模板文件
    template = {
        "_comment": "这是一个数据模板，请根据实际情况填写各字段",
        "halls": halls,
        "_usage": "为每个大厅创建独立的JSON文件，命名为 data/hall_{hallId}.json"
    }

    # 写入文件
    output_path = os.path.join(os.getcwd(), args.output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    print(f"✅ 数据结构模板已生成：{args.output}")
    print(f"✅ 共生成 {args.hall_count} 个大厅的数据模板")
    print("\n下一步：")
    print("1. 编辑模板文件，填写实际数据")
    print("2. 为每个大厅创建独立的JSON文件：data/hall_001.json, data/hall_002.json, ...")
    print(f"3. 将填写后的文件放入 data/ 目录")


if __name__ == "__main__":
    main()
