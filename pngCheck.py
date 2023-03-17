# pngCheck.py 的作用是检查via文件中图片格式是否正确
# python pngCheck.py --riseHand_via_dataset ./riseHand_via_dataset
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--riseHand_via_dataset', default='./riseHand_via_dataset',type=str)
arg = parser.parse_args()
riseHand_Dataset = arg.riseHand_via_dataset

# 循环 读出所有json文件            
for root, dirs, files in os.walk(riseHand_Dataset, topdown=False):
    for name in files:
        if not '.png' in name :
            if not '.json' in name:
                print(os.path.join(root, name))
