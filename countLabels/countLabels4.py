'''
输入参数是yolo数据集的路径，如：
python countLabels4.py /path/to/yolo/dataset

输出示例：
Class   Train   Val     Total
0       57164   15298   72462
1       46872   12060   58932
2       93509   24019   117528
3       4314    1025    5339
4       3336    847     4183
5       3287    814     4101
6       3710    953     4663
7       536     144     680
Total   212728  54160   266888

其中，"Class"表示类别标签，"Train"表示训练集中该标签数量，"Val"表示验证集中该标签数量。

'''

import os
import argparse

def count_labels(yolo_path):
    class_dict = {}
    train_labels = os.path.join(yolo_path, "labels", "train")
    val_labels = os.path.join(yolo_path, "labels", "val")

    # 统计训练集标签
    for label_file in os.listdir(train_labels):
        with open(os.path.join(train_labels, label_file), "r") as f:
            for line in f:
                class_id = line.split()[0]
                if class_id in class_dict:
                    class_dict[class_id]["train"] += 1
                else:
                    class_dict[class_id] = {"train": 1, "val": 0}

    # 统计验证集标签
    for label_file in os.listdir(val_labels):
        with open(os.path.join(val_labels, label_file), "r") as f:
            for line in f:
                class_id = line.split()[0]
                if class_id in class_dict:
                    class_dict[class_id]["val"] += 1
                else:
                    class_dict[class_id] = {"train": 0, "val": 1}

    # 获取最大类别ID
    max_class = max(int(class_id) for class_id in class_dict.keys()) if class_dict else -1

    # 按类别ID排序并计算总和
    total_train = 0
    total_val = 0
    total_all = 0
    
    print("Class\tTrain\tVal\tTotal")
    # 按顺序输出每个类别
    for i in range(max_class + 1):
        class_id = str(i)
        if class_id in class_dict:
            train = class_dict[class_id]["train"]
            val = class_dict[class_id]["val"]
            total = train + val
            print(f"{class_id}\t{train}\t{val}\t{total}")
            
            total_train += train
            total_val += val
            total_all += total
        else:
            print(f"{i}\t0\t0\t0")
    
    # 输出总和行
    print(f"Total\t{total_train}\t{total_val}\t{total_all}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count class labels in YOLO dataset')
    parser.add_argument('yolo_path', type=str, help='Path to YOLO dataset')
    args = parser.parse_args()

    count_labels(args.yolo_path)
