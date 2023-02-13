# 该文件的作用就是是检查via中的框的数量和yolo格式数据集的框的数量是否一致
# python check.py --via_Dataset ./riseHand_via_dataset --yolo_Dataset ./riseHand_Dataset
import os
import json
import cv2
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--via_Dataset', default='./riseHand_via_dataset',type=str)
parser.add_argument('--yolo_Dataset', default='./riseHand_Dataset',type=str)
arg = parser.parse_args()

# yolo数据集的存放位置 yolo_Dataset
yolo_Dataset = arg.yolo_Dataset
# via数据集的存放位置 via_Dataset
via_Dataset = arg.via_Dataset

# train_label_dir 训练标签的位置
train_label_dir = os.path.join(yolo_Dataset,'labels/train')
# val_label_dir 测试标签的位置
val_label_dir = os.path.join(yolo_Dataset,'labels/val')

# countBox 是计算 json 文件中 每张图片对应多少框
def countBox(json,root):
    # 循环读出每一个框的信息，并且图片和框的数量存放在 dict 中
    dict={}
    for i in json['metadata']:
        # 读取vid，一张图片中的所有框，vid是相同的
        vid = i.split('_')[0]
        # 通过 vid 找到对应的图片
        image_name = json['file'][vid]['fname']
        # 对图片中的框进行计数，如果第一次出现，进入else，计数为1，否则累加
        if image_name in dict:
            dict[image_name] = dict[image_name] + 1
        else:
            dict[image_name] = 1
    return dict

# check_yolo 是检查via中的框的数量和yolo格式数据集的框的数量是否一致
def check_yolo(dict_box):
    # 循环读取出每张图片中的检测框数量
    for image_name in dict_box:
        # 获取对应txt的名字和对应的路径
        txt_name = image_name.split('.')[0]+'.txt'
        # 由于不知道txt位于train还是val中，所以需要都生成，然后判断。
        txt_train_path = os.path.join(train_label_dir,txt_name)
        txt_val_path = os.path.join(val_label_dir,txt_name)
        # 判断图片是在 train 中，还是在 val 中 
        if os.path.exists(txt_train_path):
            txt_path = txt_train_path
        elif os.path.exists(txt_val_path):
            txt_path = txt_val_path
        else:
            # 如果txt不存在于train或者val中，报错
            print("no exists:")
            print(txt_train_path)
            print(txt_val_path)
            input()
        # 读取txt，计算出有多少行，每一行就代表一个框
        txt_file = open(txt_path)
        lines = len(txt_file.readlines())
        # 判断via中框的数量与txt的框的数量是否匹配。
        if not lines == dict_box[image_name]:
            print("error:",image_name)
            input()
        txt_file.close()
        
            
# 循环 读出所有json文件            
for root, dirs, files in os.walk(via_Dataset, topdown=False):
    for name in files:
        file_dir = os.path.join(root, name)
        if '.json' in name:
            file_json = open(file_dir, 'r')
            file_json_content = json.loads(file_json.read())
            dict_box = countBox(file_json_content,root)
            file_json.close()
            check_yolo(dict_box)
            print(name)
            
