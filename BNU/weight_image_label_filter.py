
# 本脚本的作用是将yolo_behavior_Dataset_all3_filter中称重的是图片和标签找到，然后再复制一次，即过采样
# python weight_image_label_filter.py --Dataset_path yolo_behavior_Dataset_all3_filter --new_Dataset_path yolo_behavior_Dataset_all4_data_enhance
import os
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--Dataset_path', default='./yolo_behavior_Dataset_all3_filter',type=str)
parser.add_argument('--new_Dataset_path', default='./yolo_behavior_Dataset_all4_data_enhance',type=str)

arg = parser.parse_args()

Dataset_path = arg.Dataset_path
new_Dataset_path = arg.new_Dataset_path

# 遍历yolo_behavior_Dataset_all3_filter文件夹下的labels。
for root, dirs, files in os.walk(os.path.join(Dataset_path, 'labels'), topdown=False):
    for name in files:
        if name.endswith('.txt'):
            # 打开labels下面的txt，然后查看其中的是否有称重的id,称重的id为0
            txtPath = os.path.join(root,name)
            with open(txtPath) as file:
                lines = file.readlines()
                for line in lines:
                    behavior_id = int(line.split(' ')[0])
                    # 如果 behavior_id 等于 0，那么就进行复制操作，但是需要对复制后的文件重新命名，
                    # 命名规则，如文件名为：01_057.txt，重新命名为01_057c.txt
                    if behavior_id == 0:
                        # 图片和文本复制到new_Dataset_path中
                        txt_name = name.split('.')[0]
                        txt_name_copy = txt_name + 'c.txt'

                        if 'train' in root:
                            train_val = 'train'
                        else:
                            train_val = 'val'
                        # 复制文本
                        shutil.copy(os.path.join(root, name), os.path.join(new_Dataset_path, 'labels', train_val, txt_name_copy))
                        # 图片路径
                        image_path = os.path.join(root, txt_name + '.jpg').replace('labels', 'images')
                        image_name_copy = txt_name + 'c.jpg'
                        # 复制图片
                        shutil.copy(image_path, os.path.join(new_Dataset_path, 'images', train_val, image_name_copy))

                        break
                