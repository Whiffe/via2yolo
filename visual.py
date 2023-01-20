# python visual.py --Dataset_dir ./Dataset --Visual_dir ./Visual
# 本代码的作用可视化yolo数据
import os
import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--Dataset_dir', default='./Dataset',type=str)
parser.add_argument('--Visual_dir', default='./Visual',type=str)

arg = parser.parse_args()
Dataset_dir = arg.Dataset_dir
Visual_dir = arg.Visual_dir

# 创建 Visual_dir
os.system('mkdir -p '+Visual_dir)
# 清空 Visual_dir
os.system('rm -r '+Visual_dir+'/*')

train_label_path = os.path.join(Dataset_dir,'labels/train')
train_image_path = os.path.join(Dataset_dir,'images/train')
val_label_path = os.path.join(Dataset_dir,'labels/val')
val_image_path = os.path.join(Dataset_dir,'images/val')

            
#坐标转换，原始存储的是YOLOv5格式
# Convert nx4 boxes from [x, y, w, h] normalized to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
def xywh2xyxy(x, w1, h1, img):
    labels = ['s1', 's2', 's3']
    label, x, y, w, h = x
    
    #边界框反归一化
    x_t = x*w1
    y_t = y*h1
    w_t = w*w1
    h_t = h*h1

    #计算坐标
    top_left_x = x_t - w_t / 2
    top_left_y = y_t - h_t / 2
    bottom_right_x = x_t + w_t / 2
    bottom_right_y = y_t + h_t / 2
    
    return int(top_left_x),int(top_left_y),int(bottom_right_x),int(bottom_right_y)

# 将 train 中的可视化
for root, dirs, files in os.walk(train_label_path, topdown=False):
    # 循环遍历出所有的txt
    for name in files:
        txt_path = os.path.join(root, name)
        if '.txt' in name:
            
            file_txt = open(txt_path, 'r')
            
            # 读出txt中的数据
            lb = np.array([x.split() for x in file_txt.read().strip().splitlines()], dtype=np.float32)  # labels
            
            image_name = name.split('.')[0]+'.png'
            image_path = os.path.join(train_image_path, image_name)
            # 读取图像文件
            img = cv2.imread(image_path)
            h, w = img.shape[:2]
            
            for x in lb:
                # 反归一化并得到左上和右下坐标，画出矩形框
                x1,y1,x2,y2 = xywh2xyxy(x, w, h, img)
                # 绘图  rectangle()函数需要坐标为整数，xywh2xyxy返回值已经是整数了。
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            visual_img_path = os.path.join(Visual_dir, image_name)
            # 将处理后的图片存储
            cv2.imwrite(visual_img_path,img)

# 将 val 中的可视化
for root, dirs, files in os.walk(val_label_path, topdown=False):
    for name in files:
        txt_path = os.path.join(root, name)
        if '.txt' in name:
            file_txt = open(txt_path, 'r')
            lb = np.array([x.split() for x in file_txt.read().strip().splitlines()], dtype=np.float32)  # labels
            
            image_name = name.split('.')[0]+'.png'
            image_path = os.path.join(val_image_path, image_name)
            # 读取图像文件
            img = cv2.imread(image_path)
            h, w = img.shape[:2]
            
            for x in lb:
                # 反归一化并得到左上和右下坐标，画出矩形框
                x1,y1,x2,y2 = xywh2xyxy(x, w, h, img)
                # 绘图  rectangle()函数需要坐标为整数，xywh2xyxy返回值已经是整数了。
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            visual_img_path = os.path.join(Visual_dir, image_name)
            cv2.imwrite(visual_img_path,img)

