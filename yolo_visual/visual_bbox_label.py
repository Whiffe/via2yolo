# python visual_bbox_label.py --yolo_Dataset yolo_behavior_Dataset-2023-12-8 --Visual_dir ./Visual
import os
import numpy as np
import cv2
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--yolo_Dataset', default='./riseHand_Dataset',type=str)
parser.add_argument('--Visual_dir', default='./Visual',type=str)

arg = parser.parse_args()
yolo_Dataset = arg.yolo_Dataset
Visual_dir = arg.Visual_dir

# 清空 Visual_dir 下的文件及文件夹
if os.path.exists(Visual_dir):
    shutil.rmtree(Visual_dir)

# 在 Visual_dir 下创建 labels images train val
os.makedirs(Visual_dir)

train_label_path = os.path.join(yolo_Dataset,'labels/train')
train_image_path = os.path.join(yolo_Dataset,'images/train')
val_label_path = os.path.join(yolo_Dataset,'labels/val')
val_image_path = os.path.join(yolo_Dataset,'images/val')

labels_class = ['blow the balloon', 'clamp', 'set the direction', 'loose clip']

# 坐标转换，原始存储的是YOLOv5格式
# Convert nx4 boxes from [x, y, w, h] normalized to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
def xywh2xyxy(x, w1, h1, img):
    label, x, y, w, h = x
    
    # 边界框反归一化
    x_t = x * w1
    y_t = y * h1
    w_t = w * w1
    h_t = h * h1

    # 计算坐标
    top_left_x = x_t - w_t / 2
    top_left_y = y_t - h_t / 2
    bottom_right_x = x_t + w_t / 2
    bottom_right_y = y_t + h_t / 2
    
    return int(top_left_x), int(top_left_y), int(bottom_right_x), int(bottom_right_y)

# 读取标签文件，获取标签类别和候选框信息
def read_labels(file):
    labels = []
    with open(file, 'r') as f:
        for line in f.readlines():
            label = line.split()
            label[0] = int(label[0])
            label[1:] = map(float, label[1:])
            labels.append(label)
    return labels

# 将 train 中的可视化
for root, dirs, files in os.walk(train_label_path, topdown=False):
    # 循环遍历出所有的txt
    for name in files:
        txt_path = os.path.join(root, name)
        if '.txt' in name:
            labels = read_labels(txt_path)
            
            image_name = name.split('.')[0] + '.jpg'
            image_path = os.path.join(train_image_path, image_name)
            # 读取图像文件
            img = cv2.imread(image_path)
            h, w = img.shape[:2]
            
            for x in labels:
                # 反归一化并得到左上和右下坐标，画出矩形框
                x1, y1, x2, y2 = xywh2xyxy(x, w, h, img)
                # 绘图  rectangle()函数需要坐标为整数，xywh2xyxy返回值已经是整数了。
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # 显示标签
                class_id = x[0]
                # cv2.putText(img, labels_class[class_id], (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                # 找出文本框的宽度和高度
                (text_width, text_height), _ = cv2.getTextSize(labels_class[class_id], cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)

                # 绘制矩形框
                cv2.rectangle(img, (x1, y1), (x1 + text_width, y1 + text_height + 30), (0, 255, 0), -1)

                # 绘制文本
                cv2.putText(img, labels_class[class_id], (x1, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

            visual_img_path = os.path.join(Visual_dir, image_name)
            # 将处理后的图片存储
            cv2.imwrite(visual_img_path, img)

# 将 val 中的可视化
for root, dirs, files in os.walk(val_label_path, topdown=False):
    for name in files:
        txt_path = os.path.join(root, name)
        if '.txt' in name:
            labels = read_labels(txt_path)
            
            image_name = name.split('.')[0] + '.jpg'
            image_path = os.path.join(val_image_path, image_name)
            # 读取图像文件
            img = cv2.imread(image_path)
            h, w = img.shape[:2]
            
            for x in labels:
                # 反归一化并得到左上和右下坐标，画出矩形框
                x1, y1, x2, y2 = xywh2xyxy(x, w, h, img)
                # 绘图  rectangle()函数需要坐标为整数，xywh2xyxy返回值已经是整数了。
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # 显示标签
                label = labels[x[0]]
                class_name = labels[x[0]][0]
                cv2.putText(img, labels[class_name], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            visual_img_path = os.path.join(Visual_dir, image_name)
            cv2.imwrite(visual_img_path, img)
