'''
python merge_class.py --dataset1_num_class 5
本脚本的作用是将两个数据集合并在一起，通常第一个数据集有多个行为，第二个数据集有一个行为
如第一个数据集：[量距离、定夹角、放小车、记录行驶时间、换轮胎]
第二个数据集：[做记录]
'''
import os
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--dataset1_num_class' ,type=str)
arg = parser.parse_args()

dataset1_num_class = arg.dataset1_num_class

dataset1_dir = './yolo-2024-2-16'
dataset2_dir = './record_all_2024_1_25'
save_dir = './merge_dataset_2024-4-15'

# 先判断save_dir 是否存在，存在就删除，然后创建
if os.path.exists(save_dir):
     shutil.rmtree(save_dir)
try:
    os.mkdir(save_dir)
except:
    pass

# save_dir下有如下目录文件夹{images,labels}/{train/val}
os.mkdir(os.path.join(save_dir, 'images'))
os.mkdir(os.path.join(save_dir, 'labels'))
os.mkdir(os.path.join(save_dir, 'images/train'))
os.mkdir(os.path.join(save_dir, 'images/val'))
os.mkdir(os.path.join(save_dir, 'labels/train'))
os.mkdir(os.path.join(save_dir, 'labels/val'))

for root, dirs, files in os.walk(dataset2_dir):
    for name in files:
        if name.endswith('.txt'):
            txt_path = os.path.join(root, name)
            with open(txt_path, 'r') as f:
                for line in f.readlines():
                    line = line[1:]
                    line = dataset1_num_class + ' ' + line
                    
                    save_txt_path = txt_path.replace(dataset2_dir, save_dir)
                    # 如果文件不存在就创建写入，如果存在就追加写入：
                    if not os.path.exists(save_txt_path):
                        with open(save_txt_path, 'w') as f:
                            f.write(line)
                    else:
                        with open(save_txt_path, 'a') as f:
                            f.write(line)