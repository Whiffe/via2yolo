# python count_dataset_class_num.py --dataset_path ./4.2k_HRW_yolo_dataset --num_class 3
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--dataset_path', default='./4.2k_HRW_yolo_dataset', type=str)
parser.add_argument('--num_class', default=3, type=int)

arg = parser.parse_args()

dataset_path = arg.dataset_path
num_class = arg.num_class


def count_class_num(labels_list,txt_path,class_num_list):
    for i in labels_list:
        file_path = os.path.join(txt_path, i)
        file = open(file_path, 'r')  # 打开文件
        file_data = file.readlines()  # 读取所有行
        for every_row in file_data:
            class_val = every_row.split(' ')[0]
            class_ind = class_list.index(int(class_val))
            class_num_list[class_ind] += 1
        file.close()
    return class_num_list

class_list = [i for i in range(num_class)]
class_num_list = [0 for i in range(num_class)]
labels_list = os.listdir(dataset_path)
txt_train_path = os.path.join(dataset_path,'labels/train')
txt_val_path = os.path.join(dataset_path,'labels/val')

labels_train_list = os.listdir(txt_train_path)
labels_val_list = os.listdir(txt_val_path)
print("train:")
print("image num:",len(labels_train_list))
print("val:")
print("image num:",len(labels_val_list))
print("All total:")
print("image num:",len(labels_train_list)+len(labels_val_list))
print("-----------")

class_num_train_list = count_class_num(labels_train_list,txt_train_path,class_num_list)
# 输出每一类的数量以及总数
print("train:")
print(class_num_train_list)
print('total:', sum(class_num_train_list))

class_num_list = [0 for i in range(num_class)]

class_num_val_list = count_class_num(labels_val_list,txt_val_path,class_num_list)
print("val:")
print(class_num_val_list)
print('total:', sum(class_num_val_list))

total_class_num_list = [i + j for i, j in zip(class_num_val_list, class_num_train_list)]


print("All total:")
print(total_class_num_list)
print('total:', sum(total_class_num_list))


