'''
python merge_class.py --change_class_id 4 --dataset_org ./record_all_2024_1_25 --dataset_change ./record-change-id-2024-5-6

本脚本的作用是将数据集中的类别ID改成另一个，目前只使用只有一个类别的数据集
如第一个数据集：[做记录] 把id 从 0 全部改成 4
'''
import os
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--change_class_id' ,type=str)
parser.add_argument('--dataset_org' ,type=str)
parser.add_argument('--dataset_change' ,type=str)
arg = parser.parse_args()

change_class_id = arg.change_class_id
dataset_org = arg.dataset_org
dataset_change = arg.dataset_change

# dataset1_dir = './yolo-2024-2-16'
# dataset2_dir = './record_all_2024_1_25'
# save_dir = './merge_dataset_2024-4-15'

# 先判断save_dir 是否存在，存在就删除，然后创建
if os.path.exists(dataset_change):
     shutil.rmtree(dataset_change)
try:
    os.mkdir(dataset_change)
except:
    pass

# save_dir下有如下目录文件夹{images,labels}/{train/val}
os.mkdir(os.path.join(dataset_change, 'images'))
os.mkdir(os.path.join(dataset_change, 'labels'))
os.mkdir(os.path.join(dataset_change, 'images/train'))
os.mkdir(os.path.join(dataset_change, 'images/val'))
os.mkdir(os.path.join(dataset_change, 'labels/train'))
os.mkdir(os.path.join(dataset_change, 'labels/val'))

for root, dirs, files in os.walk(dataset_org):
    for name in files:
        if name.endswith('.txt'):
            txt_path = os.path.join(root, name)
            with open(txt_path, 'r') as f:
                for line in f.readlines():
                    line = line[1:]
                    line = change_class_id + ' ' + line
                    
                    save_txt_path = txt_path.replace(dataset_org, dataset_change)
                    # 如果文件不存在就创建写入，如果存在就追加写入：
                    if not os.path.exists(save_txt_path):
                        with open(save_txt_path, 'w') as f:
                            f.write(line)
                    else:
                        with open(save_txt_path, 'a') as f:
                            f.write(line)