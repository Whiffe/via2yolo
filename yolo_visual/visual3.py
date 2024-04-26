# python visual3.py --yolo_Dataset SCB-exetend-BUT --Visual_dir ./Visual --labels_class ['A','B','C']  --show_label False
# mac 上运行需要修改 ['A','B','C'] 为 "['A','B','C']"
# python visual3.py --yolo_Dataset SCB-exetend-BUT --Visual_dir ./Visual --labels_class "['A','B','C']"  --show_label False
import os
import numpy as np
import cv2
import argparse
import shutil
import ast

# 定义一个函数，将输入的字符串解析为列表
def parse_list(input_str):
    try:
        # 使用ast模块的literal_eval函数来解析字符串为列表
        return ast.literal_eval(input_str)
    except (SyntaxError, ValueError):
        raise argparse.ArgumentTypeError("Invalid list format")

parser = argparse.ArgumentParser()
parser.add_argument('--yolo_Dataset', default='./riseHand_Dataset',type=str)
parser.add_argument('--Visual_dir', default='./Visual',type=str)
parser.add_argument('--labels_class', type=parse_list, help='Input a list')
parser.add_argument("--show_label", type=str, default='True', help='show label or not')

arg = parser.parse_args()
yolo_Dataset = arg.yolo_Dataset
Visual_dir = arg.Visual_dir
labels_class = arg.labels_class
show_label = arg.show_label

# 清空 Visual_dir 下的文件及文件夹
if os.path.exists(Visual_dir):
    shutil.rmtree(Visual_dir)

# 在 Visual_dir 下创建 labels images train val
os.makedirs(Visual_dir)

train_label_path = os.path.join(yolo_Dataset,'labels/train')
train_image_path = os.path.join(yolo_Dataset,'images/train')
val_label_path = os.path.join(yolo_Dataset,'labels/val')
val_image_path = os.path.join(yolo_Dataset,'images/val')

# labels_class = ['Place the candle', 'Measure distance', 'Light the candle', 'Record speed']
# labels_class = ['CJL', 'DJJ', 'FXC', 'JLXSSS', 'HLT']

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
# 设置颜色
# (255, 0, 0) 红色。 (0, 255, 0) 绿色。  (0, 0, 255) 蓝色。 (255, 255, 0) 黄色。
color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (255, 128, 0), (204, 0, 102),(0, 100 , 0), (139, 0, 139), (139, 69, 19), (160, 82, 45)]
def visual_train_val(label_path,image_path_train_val):
    for root, dirs, files in os.walk(label_path, topdown=False):
        # 循环遍历出所有的txt
        for name in files:
            txt_path = os.path.join(root, name)
            if '.txt' in name:
                labels = read_labels(txt_path)
                image_name = name.split('.')[0] + '.jpg'
                image_path = os.path.join(image_path_train_val, image_name)
                print("image_path:",image_path)
                # 读取图像文件
                img = cv2.imread(image_path)
                h, w = img.shape[:2]
                for x in labels:
                    # 反归一化并得到左上和右下坐标，画出矩形框
                    x1, y1, x2, y2 = xywh2xyxy(x, w, h, img)
                    # 显示标签
                    class_id = x[0]
                    # 绘图  rectangle()函数需要坐标为整数，xywh2xyxy返回值已经是整数了。
                    
                    cv2.rectangle(img, (x1, y1), (x2, y2),color[class_id])
                    # cv2.putText(img, labels_class[class_id], (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    
                    # 找出文本框的宽度和高度
                    (text_width, text_height), _ = cv2.getTextSize(labels_class[class_id], cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2)


                    if show_label == 'True':
                        # 绘制矩形框
                        cv2.rectangle(img, (x1, y1), (x1 + text_width, y1 + text_height + 30), color[class_id], -1)
                        # 绘制文本
                        cv2.putText(img, labels_class[class_id], (x1, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 2)

                visual_img_path = os.path.join(Visual_dir, image_name)
                # 将处理后的图片存储
                cv2.imwrite(visual_img_path, img)


visual_train_val(val_label_path, val_image_path)
visual_train_val(train_label_path, train_image_path)
