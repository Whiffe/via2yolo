'''
python process_excel_and_copy_images.py \
    --input_dir experimental_Bridge \
    --out_dir Bridge_Behavior

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

'''

import os
import pandas as pd
import shutil
import argparse

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default='experimental_Bridge')
parser.add_argument('--out_dir', type=str, default='Bridge_Behavior')
arg = parser.parse_args()

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