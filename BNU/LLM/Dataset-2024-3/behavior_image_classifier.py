'''
python behavior_image_classifier.py \
    --input_dir experimental_Bridge \
    --out_dir Bridge_Behavior \
    --prompt_file ./bridge_behavior.txt \
    --json_path ./Bridge_Behavior.json

该脚本用于从指定的输入目录（input_dir）中遍历所有以 _behavior.xlsx 结尾的 Excel 文件，
读取其中的图片名和行为标签信息，根据预设的行为类别映射，将对应的图片复制到输出目录（out_dir）下相应行为类别的子文件夹中，
同时在操作前会对输出目录进行清理或创建。


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

生成json文件
josn示例如下：
[
    {
        "messages": [
            {
                "content": "<image>"+prompt,
                "role": "user"
            },
            {
                "content": "Weighing_Objects",
                "role": "assistant"
            }
        ],
        "images": [
            "Bridge_Behavior/Weighing_Objects/0001_000002.jpg"
        ]
    },
    {
        "messages": [
            {
                "content": "<image>"+prompt,
                "role": "user"
            },
            {
                "content": "Weighing_Objects",
                "role": "assistant"
            }
        ],
        "images": [
            "Bridge_Behavior/Weighing_Objects/0001_000003.jpg"
        ]
    },
    ...


'''
import os
import pandas as pd
import shutil
import argparse
import json

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default='experimental_Bridge')
parser.add_argument('--out_dir', type=str, default='Bridge_Behavior')
parser.add_argument('--prompt_file', type=str, default='./bridge_behavior.txt', help='Path to the prompt file')
parser.add_argument('--json_path', type=str, default='./Bridge_Behavior/Bridge_Behavior.json', help='Path to save the JSON file')
arg = parser.parse_args()

# 读取 prompt
try:
    with open(arg.prompt_file, 'r', encoding='utf-8') as f:
        prompt = f.read().strip()
except FileNotFoundError:
    print(f"Error: Prompt file {arg.prompt_file} not found.")
    exit(1)

# 定义类别映射
category_mapping = {
    0: "Measuring_Distance",  # 测距离
    1: "Placing_Boards",  # 放板子
    2: "Placing_Objects",  # 放重物
    3: "Weighing_Objects",  # 称重物
    4: "Record"  # 记数据
}

# 检查并处理输出目录
if os.path.exists(arg.out_dir):
    # 清除输出目录下的所有内容
    for root, dirs, files in os.walk(arg.out_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
else:
    # 创建输出目录
    os.makedirs(arg.out_dir)

# 创建类别子文件夹
for category in category_mapping.values():
    category_dir = os.path.join(arg.out_dir, category)
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)

# 遍历 input_dir 文件夹下的子文件夹
for root, dirs, files in os.walk(arg.input_dir):
    for file in files:
        if file.endswith("_behavior.xlsx"):
            excel_path = os.path.join(root, file)
            print("excel_path:", excel_path)
            df = pd.read_excel(excel_path)
            for index, row in df.iterrows():
                image_name = row.iloc[0]
                # 检查是否有行为标签
                for col in row[1:]:
                    if pd.notna(col):
                        category = category_mapping[int(col)]
                        category_dir = os.path.join(arg.out_dir, category)
                        image_path = os.path.join(root, f"{image_name}.jpg")
                        if os.path.exists(image_path):
                            shutil.copy2(image_path, category_dir)
                        else:
                            print(f"图片 {image_path} 不存在。")

# 输出每个类别文件夹下图片的数量
print("\n每个类别文件夹下图片的数量：")
for category in category_mapping.values():
    category_dir = os.path.join(arg.out_dir, category)
    image_count = len([f for f in os.listdir(category_dir) if os.path.isfile(os.path.join(category_dir, f))])
    print(f"{category}: {image_count} 张图片")

# 生成 JSON 数据
json_data = []
for category in category_mapping.values():
    category_dir = os.path.join(arg.out_dir, category)
    for image_file in os.listdir(category_dir):
        if os.path.isfile(os.path.join(category_dir, image_file)):
            image_path = os.path.join(arg.out_dir, category, image_file)
            item = {
                "messages": [
                    {
                        "content": "<image>" + prompt,
                        "role": "user"
                    },
                    {
                        "content": category,
                        "role": "assistant"
                    }
                ],
                "images": [
                    image_path
                ]
            }
            json_data.append(item)

# 保存 JSON 文件
json_file_path = arg.json_path
json_dir = os.path.dirname(json_file_path)
if not os.path.exists(json_dir):
    os.makedirs(json_dir)
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

print(f"\nJSON 文件已生成：{json_file_path}")