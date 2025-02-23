'''
python imgs2oneFolder.py --input_dir experimental_Bridge --out_dir Bridge_Behavior

imgs2oneFolder.py的作用是将标注的数据集中的所有图片，复制到一个文件夹中去。
'''

import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default='experimental_Bridge')
parser.add_argument('--out_dir', type=str, default='Bridge_Behavior')
arg = parser.parse_args()

# 源文件夹路径
source_folder = arg.input_dir
# 目标文件夹路径
target_folder = arg.out_dir

# 如果目标文件夹不存在，创建它
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 遍历源文件夹及其子文件夹
for root, dirs, files in os.walk(source_folder):
    for file in files:
        # 检查文件扩展名是否为图片文件
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            source_file_path = os.path.join(root, file)
            target_file_path = os.path.join(target_folder, file)
            # 复制文件
            shutil.copy2(source_file_path, target_file_path)
