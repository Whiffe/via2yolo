'''
python generate_json.py \
    --out_dir Bridge_Behavior \
    --prompt_file ./bridge_behavior.txt \
    --json_path ./Bridge_Behavior/Bridge_Behavior.json

`generate_json.py` 脚本的功能是根据指定的输出目录、提示文件路径和 JSON 保存路径，
读取提示信息，遍历输出目录下的类别文件夹，为每个文件夹中的图片生成包含用户提示和对应类别信息的 JSON 对象，并将这些对象保存为指定路径的 JSON 文件。    

'''
import os
import argparse
import json

# 解析命令行参数
parser = argparse.ArgumentParser()
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

# 生成 JSON 数据
json_data = []
# 遍历输出目录下的所有文件夹，这些文件夹名即为类别
for category in os.listdir(arg.out_dir):
    category_dir = os.path.join(arg.out_dir, category)
    if os.path.isdir(category_dir):
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