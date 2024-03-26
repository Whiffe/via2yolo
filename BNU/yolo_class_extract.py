'''
从SCB-exetend中提取出我们想要的类别，生成新的数据集。
python yolo_class_extract.py --original_dataset_dir ./yolo-2024-2-16/ --new_dataset_dir ./yolo-2024-3-16-R/ --desired_classes [3] --class_mapping {3:0}
python yolo_class_extract.py --original_dataset_dir ./yolo-2024-2-16/ --new_dataset_dir ./yolo-2024-3-16-MMRC/ --desired_classes [0,1,2,4] --class_mapping {0:0,1:1,2:2,4:3}

python yolo_class_extract.py --original_dataset_dir ./yolo-2024-3-25/ --new_dataset_dir ./yolo-2024-3-25-R/ --desired_classes [3] --class_mapping {3:0}
python yolo_class_extract.py --original_dataset_dir ./yolo-2024-3-25/ --new_dataset_dir ./yolo-2024-3-25-MMRC/ --desired_classes [0,1,2,4] --class_mapping {0:0,1:1,2:2,4:3}


'''
import os
import shutil
import argparse
import ast

# 定义一个函数，将输入的字符串解析为列表
def parse_list(input_str):
    try:
        # 使用ast模块的literal_eval函数来解析字符串为列表
        return ast.literal_eval(input_str)
    except (SyntaxError, ValueError):
        raise argparse.ArgumentTypeError("Invalid list format")


# 定义一个函数，将输入的字符串解析为字典
def parse_dict(input_str):
    try:
        # 使用ast模块的literal_eval函数来解析字符串为字典
        return ast.literal_eval(input_str)
    except (SyntaxError, ValueError):
        raise argparse.ArgumentTypeError("Invalid dictionary format")


parser = argparse.ArgumentParser()
parser.add_argument('--original_dataset_dir', default='./yolo_behavior_Dataset-2024-3-25/',type=str)
parser.add_argument('--new_dataset_dir', default='./yolo-2024-3-25-R/',type=str)
parser.add_argument('--desired_classes', type=parse_list, help='Input a list')
parser.add_argument('--class_mapping', type=parse_dict, help='Input a dictionary')


arg = parser.parse_args()
original_dataset_dir = arg.original_dataset_dir
new_dataset_dir = arg.new_dataset_dir
desired_classes = arg.desired_classes
class_mapping = arg.class_mapping



# 定义原始数据集目录和新数据集目录
# original_dataset_dir = './yolo-2024-3-22-org/'
# original_dataset_dir = './yolo-2024-2-16/'
# original_dataset_dir = './yolo_behavior_Dataset-2024-3-25/'

# new_dataset_dir = './yolo-2024-3-22-R/'
# new_dataset_dir = './yolo-2024-3-25-R/'
# new_dataset_dir = './yolo-2024-3-22-MMRC/'
# new_dataset_dir = './yolo-2024-3-25-MMRC/'

# names: ['Measure distance', 'Measure angle', 'Release a car', 'Record travelling time', 'change tyres']
# names: ['Measure distance', 'Measure angle', 'Release a car', 'change tyres']
# names: ['Record travelling time']

# 定义你想要的类别
# 注意这是原版yolo的类别标签，即选取你想要原版yolo的哪些类别标签
# desired_classes = [0, 1, 2, 3]
# desired_classes = [3] # Record travelling time
# desired_classes = [0, 1, 2, 4] # 'Measure distance', 'Measure angle', 'Release a car', 'change tyres'

# 新类别标签映射
# key: value格式，key是原版yolo的类别标签，value是你想映射成的类别标签
# class_mapping = {0: 0, 1: 0, 2: 1, 3: 2}
# class_mapping = {3: 0}
# class_mapping = {0:0, 1:1, 2:2, 4:3}

# 创建新数据集目录
os.makedirs(new_dataset_dir, exist_ok=True)

# 遍历train和val文件夹
for split in ['train', 'val']:
    split_original_labels_dir = os.path.join(original_dataset_dir, 'labels', split)
    split_original_images_dir = os.path.join(original_dataset_dir, 'images', split)

    split_new_labels_dir = os.path.join(new_dataset_dir, 'labels', split)
    split_new_images_dir = os.path.join(new_dataset_dir, 'images', split)

    os.makedirs(split_new_labels_dir, exist_ok=True)
    os.makedirs(split_new_images_dir, exist_ok=True)

    # 遍历当前split下的所有txt文件
    for root, dirs, files in os.walk(split_original_labels_dir):
        for file in files:
            if file.endswith('.txt'):
                with open(os.path.join(root, file), 'r') as f:
                    lines = f.readlines()
                    filtered_lines = []
                    for line in lines:
                        class_index = int(line.split()[0])
                        if class_index in desired_classes:
                            # 更新类别标签
                            new_class_index = class_mapping[class_index]
                            filtered_lines.append(f"{new_class_index} {' '.join(line.split()[1:])}\n")

                # 写入新的txt文件
                if filtered_lines:
                    with open(os.path.join(split_new_labels_dir, file), 'w') as f:
                        f.writelines(filtered_lines)

                    # 复制对应的图像文件到新数据集目录中
                    image_filename = file.replace('.txt', '.jpg')
                    original_image_path = os.path.join(split_original_images_dir, image_filename)
                    new_image_path = os.path.join(split_new_images_dir, image_filename)
                    shutil.copy(original_image_path, new_image_path)
