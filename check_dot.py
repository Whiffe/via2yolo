# 这一段代码是将找到小点对应的图片名字（图片名字中包含路径信息）
# python check_dot.py --dot_size 15 --via_Dataset ./riseHand_via_dataset
import os
import json
import argparse

parser = argparse.ArgumentParser()
# dot_size 是调整筛选小点的阈值
parser.add_argument('--dot_size', default=15,type=int)
parser.add_argument('--via_Dataset', default='./riseHand_via_dataset',type=str)

arg = parser.parse_args()

dot_size = arg.dot_size
via_Dataset = arg.via_Dataset

# 计数有多少小点
dot_num = 0

# countBox 是计算 json 文件中 每张图片对应多少框
def search_dot(json,root):
    global dot_num
    # 循环读出每一个框的信息，并且图片和框的数量存放在 dict 中
    dict={}
    for i in json['metadata']:
        # 读取vid，一张图片中的所有框，vid是相同的
        vid = i.split('_')[0]
        # 自动化标注的数据中，有image这个字符串，所以需要再次提取
        if 'image' in vid:
            vid = vid.split('image')[-1]
        # 通过 vid 找到对应的图片
        image_name = json['file'][vid]['fname']
        # 读取坐标信息
        xy = json['metadata'][i]['xy']
        # xy[3]，xy[4]是w h，如果 w 或者 h 都小于阈值，则判定为小点
        if float(xy[3])<dot_size or float(xy[4])<dot_size:
            print("dot:",image_name)
            dot_num = dot_num +1

# 循环 读出所有json文件            
for root, dirs, files in os.walk(via_Dataset, topdown=False):
    for name in files:
        file_dir = os.path.join(root, name)
        if '.json' in name:
            file_json = open(file_dir, 'r')
            file_json_content = json.loads(file_json.read())
            search_dot(file_json_content,root)
            
print("dot_num:",dot_num)
