# python countLabels2.py --dir_path riseHand_Dataset
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

# 新增变量
count_1_2 = 0
count_3_5 = 0
count_6_10 = 0
count_11_15 = 0
count_16_20 = 0
count_21_above = 0

# 计算每个txt文件的行数并进行区间统计
for txt_file in txt_files:
    with open(txt_file, 'r') as f:
        file_lines = f.readlines()
        content_lines = len([line for line in file_lines if line.strip()]) # 计算文件中有内容的总行数

        # 统计各个区间的txt文件数量
        if content_lines <= 2:
            count_1_2 += 1
        elif content_lines <= 5:
            count_3_5 += 1
        elif content_lines <= 10:
            count_6_10 += 1
        elif content_lines <= 15:
            count_11_15 += 1
        elif content_lines <= 20:
            count_16_20 += 1
        else:
            count_21_above += 1

        # 输出每个txt的行数区间
        label = os.path.basename(txt_file) # 获取txt文件的文件名
        print(label + "：", end='') # 输出文件名
        if content_lines <= 2:
            print("1-2行")
        elif content_lines <= 5:
            print("3-5行")
        elif content_lines <= 10:
            print("6-10行")
        elif content_lines <= 15:
            print("11-15行")
        elif content_lines <= 20:
            print("16-20行")
        else:
            print("21行及以上")

# 输出各个区间txt文件数量
print("在各个行数区间的txt文件数量分别为：")
print("1-2行：", count_1_2)
print("3-5行：", count_3_5)
print("6-10行：", count_6_10)
print("11-15行：", count_11_15)
print("16-20行：", count_16_20)
print("21行及以上：", count_21_above)
