# 这一段代码是将via转化为yolo格式
# python via2yolo3.py --via_Dataset  ./RRW_via_Dataset/ --yolo_Dataset ./yolo_Dataset --tain_r 0.8
# 注意这是 via 中多个动作（以看书写字举手为例）转化为yolo格式
# 并且可以检查没有标注的框，并给出没有标注的图片

import os
import json
import cv2
import random
import argparse
import shutil

parser = argparse.ArgumentParser()

parser.add_argument('--via_Dataset', default='./via_Dataset', type=str)
parser.add_argument('--yolo_Dataset', default='./yolo_Dataset', type=str)
parser.add_argument('--tain_r', default=0.8, type=float)

arg = parser.parse_args()

via_Dataset = arg.via_Dataset

# yolo数据集的存放位置 Dataset_dir
yolo_Dataset = arg.yolo_Dataset

# 删除 Dataset_dir 文件夹
if os.path.exists(yolo_Dataset):
    shutil.rmtree(yolo_Dataset)
# 在 Dataset_dir 下创建 labels images train val
os.makedirs(yolo_Dataset + '/labels/train')
os.makedirs(yolo_Dataset + '/labels/val')
os.makedirs(yolo_Dataset + '/images/train')
os.makedirs(yolo_Dataset + '/images/val')



# 训练集与验证集的比例，tain_r代表训练集的比例，1-tain_r 代表验证集的比例
tain_r = arg.tain_r
# 设置 labels images train val 的路径
train_label_dir = yolo_Dataset + '/labels/train/'
val_label_dir = yolo_Dataset + '/labels/val/'
train_image_dir = yolo_Dataset + '/images/train/'
val_image_dir = yolo_Dataset + '/images/val/'


# via2yolo 函数是将via信息转化为yolo的格式·
def via2yolo(json, root):
    # 循环读出每一个框的信息
    for i in json['metadata']:
        # 从 i 中获取 vid
        print("i",i)
        vid = i.split('_')[0]
        if 'image' in vid:
            vid = vid.split('image')[-1]
        # 获取对应的图片名字
        print("vid",vid)
        image_name = json['file'][vid]['fname']
        print("image_name",image_name)
        input()
        # 获取图片的路径
        # 由于图片是一个链接，所以就取链接的最后一个 / 后面的内容
        image_dir = os.path.join(root, image_name.split('/')[-1])


        # 读取图片的高和宽
        img = cv2.imread(image_dir)
        h = img.shape[0]
        w = img.shape[1]

        # 读取 via 中的 坐标 xywh，框的左上角坐标 x y，与框的宽高
        xywh = json['metadata'][i]['xy'][1:]

        # 获取动作的id

        try:
            action_id = json['metadata'][i]['av']['1']
        except KeyError:
            print(json['metadata'][i]['av'])
            print("下面的图片中有没有标注的框")
            print("image_name:",image_name)
            input()


        '''
        将xywh 转化为 yolo 的格式
        第一个参数是0，代表举手这一个分类
        第二个参数是，框的中心坐标 x，归一化处理
        第三个参数是，框的中心坐标 y，归一化处理
        第四个参数是，框的宽度 w，归一化处理
        第五个参数是，框的高度 h，归一化处理
        第六个参数是，换行
        '''
        xcyc_wh = action_id + ' ' + str((xywh[0] + xywh[2] / 2) / w) + ' ' + str((xywh[1] + xywh[3] / 2) / h) + \
                  ' ' + str(xywh[2] / w) + ' ' + str(xywh[3] / h) + '\n'

        # 设置 txt 的 train 和 val 的路径
        # image_name 是一个链接，所以需要做提取
        temp_train_txt_path = os.path.join(train_label_dir, image_name.split('/')[-1].split('.')[0] + '.txt')
        temp_val_txt_path = os.path.join(val_label_dir, image_name.split('/')[-1].split('.')[0] + '.txt')

        '''
        判断当前的 temp_train_txt_path 或者 temp_val_txt_path 是否已经存在
        如果不存在，就进入 if 中
        不存在代表已经进入下一个图片的框了，需要创建一个新的txt
        如果存在，就进入 else 中
        '''
        if not (os.path.isfile(temp_train_txt_path) or os.path.isfile(temp_val_txt_path)):
            # 这里的 train 和 val 的划分 采用随机数方式
            # 这里会更新 txt 的路径 和图片 的路径
            # 由于图片是一个链接，所以就取链接的最后一个 / 后面的内容
            if random.random() <= tain_r:
                txt_path = temp_train_txt_path
                image_path = os.path.join(train_image_dir, image_name.split('/')[-1])
            else:
                txt_path = temp_val_txt_path
                image_path = os.path.join(val_image_dir, image_name.split('/')[-1])
            # 将图片复制到指定路径
            shutil.copy(image_dir,image_path)
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
        with open(txt_path, "a") as file:  # a，代表追加内容
            file.write(xcyc_wh)


# 循环 读出所有json文件
for root, dirs, files in os.walk(via_Dataset, topdown=False):
    for name in files:
        file_dir = os.path.join(root, name)
        if '.json' in name:
            file_json = open(file_dir, 'r')
            file_json_content = json.loads(file_json.read())
            via2yolo(file_json_content, root)
            file_json.close()
            print(file_dir)
