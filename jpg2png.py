'''
jpg2png.py 的作用是找出via文件中jpg格式的图片
由于本代码会将jpg图片转化为png格式，这就需要将原来的文件备份一次
备份的文件夹名字为：riseHand_via_dataset1
'''
# python jpg2png.py --riseHand_via_dataset ./riseHand_via_dataset --riseHand_via_dataset1 ./riseHand_via_dataset1
import os
import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--riseHand_via_dataset', default='./riseHand_via_dataset',type=str)
parser.add_argument('--riseHand_via_dataset1', default='./riseHand_via_dataset1',type=str)
arg = parser.parse_args()
riseHand_via_dataset = arg.riseHand_via_dataset

# 循环 找出非png格式、非josn的文件
for root, dirs, files in os.walk(riseHand_via_dataset, topdown=False):
    files.sort()
    for name in files:
        file_path = os.path.join(root, name)
        if '.jpg' in name:
            img = Image.open(file_path)
            new_file = os.path.splitext(name)[0] + '.png'
            # 在备份路径中转化图片
            file_path1 = file_path.replace(riseHand_via_dataset, riseHand_via_dataset+'1')
            file_path2 = file_path1.replace('.jpg', '.png')

            img.convert('RGB').save(file_path2)

            try:
                os.remove(file_path1)
            except:
                pass

            # 删除备份文件夹中jpg格式的图片

            print("change:------:",file_path1,":------------")


