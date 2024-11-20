'''
从yolo数据集中提取特定类别的数据并生成新的 YOLO 数据集，并且修改类别id
python extract_data_class.py --source_yolo_dir "../600148 别致的花灯/转化/yolo_behavior_Dataset-2024-4-5-add_pre_data" --target_yolo_dir yolo_measure --class_id_to_extract 1 --new_class_id 3
python extract_data_class.py \
    --source_yolo_dir "../600148 别致的花灯/转化/yolo_behavior_Dataset-2024-4-5-add_pre_data" \
    --target_yolo_dir yolo_measure \
    --class_id_to_extract 1 \
    --new_class_id 3
'''
import os
import shutil
import argparse

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_yolo_dir', default='../600148 别致的花灯/转化/yolo_behavior_Dataset-2024-4-5-add_pre_data', type=str)
    parser.add_argument('--target_yolo_dir', default='yolo_measure', type=str)
    parser.add_argument('--class_id_to_extract', default=1, type=int)
    parser.add_argument('--new_class_id', default=3, type=int)
    return parser.parse_args()

def extract_yolo_data(source_dir, target_dir, class_id_to_extract, new_class_id):
    # 确保目标主目录和子目录存在
    os.makedirs(os.path.join(target_dir, "images", "train"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "images", "val"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "labels", "train"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "labels", "val"), exist_ok=True)

    # 定义原始数据的路径
    images_dir = os.path.join(source_dir, "images")
    labels_dir = os.path.join(source_dir, "labels")

    # 定义目标数据的路径
    new_images_dir = os.path.join(target_dir, "images")
    new_labels_dir = os.path.join(target_dir, "labels")

    # 遍历 train 和 val 文件夹
    for split in ["train", "val"]:
        # 定义当前 split 的路径
        split_images_dir = os.path.join(images_dir, split)
        split_labels_dir = os.path.join(labels_dir, split)

        # 遍历当前 split 下的所有标签文件
        for label_file in os.listdir(split_labels_dir):
            label_path = os.path.join(split_labels_dir, label_file)
            with open(label_path, "r") as f:
                lines = f.readlines()

            # 筛选并修改目标类别的数据
            target_lines = []
            for line in lines:
                if line.startswith(f"{class_id_to_extract} "):
                    # 替换类别 ID
                    new_line = line.replace(f"{class_id_to_extract} ", f"{new_class_id} ", 1)
                    target_lines.append(new_line)

            if target_lines:
                # 如果有目标类别的数据，复制图片并生成新标签文件
                image_file = label_file.replace(".txt", ".jpg")
                image_source_path = os.path.join(split_images_dir, image_file)
                image_target_path = os.path.join(new_images_dir, split, image_file)
                shutil.copy(image_source_path, image_target_path)

                # 写入新的标签文件
                new_label_path = os.path.join(new_labels_dir, split, label_file)
                with open(new_label_path, "w") as new_f:
                    new_f.writelines(target_lines)
if __name__ == "__main__":
    configs = argparser()   # 加载参数配置
    source_yolo_dir =  configs.source_yolo_dir # 原始 YOLO 数据集路径
    target_yolo_dir = configs.target_yolo_dir  # 新生成的 YOLO 数据集路径
    class_id_to_extract = configs.class_id_to_extract  # 需要提取的类别 ID
    new_class_id = configs.new_class_id  # 修改后的类别 ID

    extract_yolo_data(source_yolo_dir, target_yolo_dir, class_id_to_extract, new_class_id)

