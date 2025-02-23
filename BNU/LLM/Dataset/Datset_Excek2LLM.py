'''
Datset_Excek2LLM.py的作用是将人工标注的Excel转化为视觉大模型的json格式，并且进行了数据平衡操作

excel的格式如下，以experimental_Bridge文件夹下的0037文件夹为例： 
0037_000001					
0037_000002					
0037_000003					
0037_000004					
0037_000005	0				
0037_000006	0				
0037_000007	0				
0037_000008					
0037_000009					
0037_000010					4
0037_000011					4
0037_000012					4
0037_000013					4
0037_000014					
....

第一列是图片名，第二到第六列分别用数字代表行为，0: "测距离", 1: "放板子", 2: "放重物", 3: "称重物", 4: "记数据"


转化后的josn示例如下：
[
    {
        "messages": [
            {
                "content": "<image>学生在做什么?请在以下类别中进行选择：测距离/放板子/放重物/称重物/记数据/其他",
                "role": "user"
            },
            {
                "content": "称重物",
                "role": "assistant"
            }
        ],
        "images": [
            "Bridge_Behavior/0001_000002.jpg"
        ]
    },
    {
        "messages": [
            {
                "content": "<image>学生在做什么?请在以下类别中进行选择：测距离/放板子/放重物/称重物/记数据/其他",
                "role": "user"
            },
            {
                "content": "称重物",
                "role": "assistant"
            }
        ],
        "images": [
            "Bridge_Behavior/0001_000003.jpg"
        ]
    },
    ...
'''

'''
python Datset_Excek2LLM.py --input_dir experimental_Bridge --out_dir ./result.json
'''

import os
import pandas as pd
import json
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default='experimental_Bridge')
parser.add_argument('--out_dir', type=str, default='./result.json')

arg = parser.parse_args()

# 定义类别映射
category_mapping = {
    0: "测距离",
    1: "放板子",
    2: "放重物",
    3: "称重物",
    4: "记数据"
}

# 定义最终的JSON数据结构
result = []

# 遍历experimental_Bridge文件夹下的子文件夹
for root, dirs, files in os.walk("experimental_Bridge"):
    for file in files:
        if file.endswith("_behavior.xlsx"):
            excel_path = os.path.join(root, file)
            print("excel_path:",excel_path)
            df = pd.read_excel(excel_path)
            for index, row in df.iterrows():
                image_name = row.iloc[0]
                category = "其他"
                for value in row.iloc[1:]:
                    if pd.notnull(value):
                        category = category_mapping[value]
                        break
                # print("category:",category)
                message = {
                    "messages": [
                        {
                            "content": "<image>学生在做什么?请在以下类别中进行选择：测距离/放板子/放重物/称重物/记数据/其他",
                            "role": "user"
                        },
                        {
                            "content": category,
                            "role": "assistant"
                        }
                    ],
                    "images": [f"Bridge_Behavior/{image_name}.jpg"]
                }
                # print(message)
                result.append(message)


# 将结果写入JSON文件
with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
# 统计每个类别的数量（平衡前）
category_counts_before = {category: 0 for category in set([item["messages"][1]["content"] for item in result])}
for item in result:
    category = item["messages"][1]["content"]
    category_counts_before[category] += 1
print("平衡前每个类别的数量:")
for category, count in category_counts_before.items():
    print(f"{category}: {count}")

