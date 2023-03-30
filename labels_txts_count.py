# python labels_txts_count.py --dir_path riseHand_Dataset

import os
import argparse

# 定义参数解析器
parser = argparse.ArgumentParser()
parser.add_argument("--dir_path", help="输入文件夹路径")
args = parser.parse_args()

# 检查是否输入了文件夹路径
if not args.dir_path:
    print("请输入文件夹路径")
    exit()

# 遍历目录下的所有txt文件，并统计个数
txt_files = [os.path.join(root, name)
             for root, dirs, files in os.walk(args.dir_path)
             for name in files if name.endswith('.txt')]
txt_count = len(txt_files)

# 计算文件中有内容的行数
total_lines = 0
for txt_file in txt_files:
    with open(txt_file, 'r') as f:
        file_lines = f.readlines()
        content_lines = len([line for line in file_lines if line.strip()]) # 计算文件中有内容的总行数
        total_lines += content_lines

# 输出结果
print("所有txt文件有内容的行数量为：", total_lines)
print("txt文件的数量为：", txt_count)
