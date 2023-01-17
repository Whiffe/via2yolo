# 这一段代码是将via转化为yolo格式
# python via2yolo.py

import os
import json
import cv2
import random

# yolo数据集的存放位置 Dataset_dir
Dataset_dir = './Dataset'
# 清空 Dataset_dir 下的文件及文件夹
os.system('rm -r '+Dataset_dir+'/*')
# 在 Dataset_dir 下创建 labels images train val
os.system('mkdir -p '+Dataset_dir+'/{labels,images}/{train,val}')

# 训练集与验证集的比例，tain_r代表训练集的比例，1-tain_r 代表验证集的比例
tain_r = 0.65
# 设置 labels images train val 的路径
train_label_dir = Dataset_dir + '/labels/train/'
val_label_dir = Dataset_dir + '/labels/val/'
train_image_dir = Dataset_dir + '/images/train/'
val_image_dir = Dataset_dir + '/images/val/'

# via2yolo 函数是将via信息转化为yolo的格式
def via2yolo(json,root):
    # 循环读出每一个框的信息
    for i in json['metadata']:
        # 从 i 中获取 vid
        vid = i.split('_')[0]
        # 获取对应的图片名字
        image_name = json['file'][vid]['fname']
        # 获取图片的路径
        image_dir = os.path.join(root, image_name) 
        
        # 读取图片的高和宽
        img = cv2.imread(image_dir)
        h = img.shape[0]
        w = img.shape[1]
        
        # 读取 via 中的 坐标 xywh，框的左上角坐标 x y，与框的宽高 
        xywh = json['metadata'][i]['xy'][1:]
        
        '''
        将xywh 转化为 yolo 的格式
        第一个参数是0，代表举手这一个分类
        第二个参数是，框的中心坐标 x，归一化处理
        第三个参数是，框的中心坐标 y，归一化处理
        第四个参数是，框的宽度 w，归一化处理
        第五个参数是，框的高度 h，归一化处理
        第六个参数是，换行
        '''
        xcyc_wh ='0 ' + str( (xywh[0]+xywh[2]/2)/w ) + ' ' + str( (xywh[1]+xywh[3]/2)/h ) +\
                ' ' + str( xywh[2]/w ) + ' ' + str( xywh[3]/h ) +'\n'

        
        # 设置 txt 的 train 和 val 的路径
        temp_train_txt_path = os.path.join(train_label_dir, image_name.split('.')[0]+'.txt')
        temp_val_txt_path = os.path.join(val_label_dir, image_name.split('.')[0]+'.txt')
        
        '''
        判断当前的 temp_train_txt_path 或者 temp_val_txt_path 是否已经存在
        如果不存在，就进入 if 中
        不存在代表已经进入下一个图片的框了，需要创建一个新的txt
        如果存在，就进入 else 中
        '''
        if not (os.path.isfile(temp_train_txt_path) or os.path.isfile(temp_val_txt_path)):
            # 这里的 train 和 val 的划分 采用随机数方式
            # 这里会更新 txt 的路径 和图片 的路径
            if random.random() <= tain_r:
                txt_path = temp_train_txt_path
                image_path = os.path.join(train_image_dir, image_name)
            else:
                txt_path = temp_val_txt_path
                image_path = os.path.join(val_image_dir, image_name)
            # 将图片复制到指定路径
            os.system('cp ' + image_dir + ' ' + image_path)
            '''
            由于via中的标注可能存在后续的添加的框，使得框的顺序会是乱的
            如果不加下放的 else 内容，会使得后续的添加的框不能放在对应的txt中，而放到了上一个循环的txt中
            所以需要在 else 中判断，当前循环的框所对应的图片名与当前的txt名是否相同，如果不同，说明出现上述问题
            那么就需要重置txt
            '''
        else:
            # 判断 当前循环的框所对应的图片名与当前的 txt 名是否相同
            if image_name.split('.')[0] == image_name.split('/')[-1].split('.')[0]:
                # 判断 重置的 txt 路径是在 train 中还是在 val 中
                if os.path.isfile(temp_train_txt_path):
                    txt_path = temp_train_txt_path
                else:
                    txt_path = temp_val_txt_path
        # 向指定txt路径追加内容
        with open(txt_path,"a") as file:   # a，代表追加内容
            file.write(xcyc_wh)

# 循环 读出所有json文件            
for root, dirs, files in os.walk("./", topdown=False):
    for name in files:
        file_dir = os.path.join(root, name)
        if '.json' in name:
            file_json = open(file_dir, 'r')
            file_json_content = json.loads(file_json.read())
            via2yolo(file_json_content,root)
            file_json.close()
            print(file_dir)
