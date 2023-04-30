 '''
输入参数是yolo数据集的路径，如：
python countLabels3.py /path/to/yolo/dataset

输出示例：
Class   Train   Val
0       4876    1236
1       3240    943
2       2474    769
3       1275    311
4       284     90
5       3612    896

其中，"Class"表示类别标签，"Train"表示训练集中该标签数量，"Val"表示验证集中该标签数量。

'''
import os
import argparse

def count_labels(yolo_path):
    class_dict = {}
    train_labels = os.path.join(yolo_path, "labels", "train")
    val_labels = os.path.join(yolo_path, "labels", "val")

    # Count train labels
    for label_file in os.listdir(train_labels):
        with open(os.path.join(train_labels, label_file), "r") as f:
            for line in f:
                class_id = line.split()[0]
                if class_id in class_dict:
                    class_dict[class_id]["train"] += 1
                else:
                    class_dict[class_id] = {"train": 1, "val": 0}

    # Count val labels
    for label_file in os.listdir(val_labels):
        with open(os.path.join(val_labels, label_file), "r") as f:
            for line in f:
                class_id = line.split()[0]
                if class_id in class_dict:
                    class_dict[class_id]["val"] += 1
                else:
                    class_dict[class_id] = {"train": 0, "val": 1}

    # Print results
    print("Class\tTrain\tVal")
    for class_id, count_dict in class_dict.items():
        print(f"{class_id}\t{count_dict['train']}\t{count_dict['val']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Count class labels in YOLO dataset')
    parser.add_argument('yolo_path', type=str, help='Path to YOLO dataset')
    args = parser.parse_args()

    count_labels(args.yolo_path)
