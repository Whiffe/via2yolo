#pngCheck.py 的作用是检查via文件中图片格式是否正确
# python pngCheck.py --riseHand_via_dataset ./riseHand_via_dataset
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--riseHand_via_dataset', default='./riseHand_via_dataset',type=str)
arg = parser.parse_args()
riseHand_via_dataset = arg.riseHand_via_dataset

# 循环 找出非png格式、非josn的文件
for root, dirs, files in os.walk(riseHand_via_dataset, topdown=False):
    files.sort()
    for name in files:
        if not '.png' in name :
            if not '.json' in name:
                file_path = os.path.join(root, name)
                print(file_path)


