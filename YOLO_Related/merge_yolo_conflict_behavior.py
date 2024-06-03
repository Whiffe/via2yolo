'''
python merge_yolo_conflict_behavior.py --detect_path SCB-yolo-TB-detect
在yolo检测中，我们会发现，同一个学生，会同时检测出看书和写字，我们知道，这两个行为是冲突的，只能存在一个
本脚本的作用就是将两个（或者多个）冲突的行为合并为1个，选择两个（或者多个）中conf最高的，其余舍弃。
'''
import argparse
import os
import shutil

def argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--detect_path', default='./SCB-yolo-TB-detect', type=str)
    parser.add_argument('--new_detect_path', default='./SCB-yolo-TB-detect2', type=str)

    return parser.parse_args()


# 读取yolo的txt文件
def read_yolo_txt(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    data = []
    for line in lines:
        parts = line.strip().split()
        cls = int(parts[0])
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])
        confidence = float(parts[5])
        data.append((cls, x_center, y_center, width, height, confidence))
    return data

# xywh转化为xyxy
def convert_to_bbox(data):
    bboxes = []
    for item in data:
        cls, x_center, y_center, width, height, confidence = item
        x1 = x_center - width / 2
        y1 = y_center - height / 2
        x2 = x_center + width / 2
        y2 = y_center + height / 2
        bboxes.append((cls, x1, y1, x2, y2, confidence))
    return bboxes

def iou(box1, box2):
    x1, y1, x2, y2 = box1
    x1_, y1_, x2_, y2_ = box2

    xi1 = max(x1, x1_)
    yi1 = max(y1, y1_)
    xi2 = min(x2, x2_)
    yi2 = min(y2, y2_)
    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2_ - x1_) * (y2_ - y1_)
    union_area = box1_area + box2_area - inter_area

    return inter_area / union_area if union_area else 0

# 找到类别不同的重叠框
def find_overlapping_boxes(bboxes, iou_threshold=0.8):
    overlapping_boxes = {}
    for i, box1 in enumerate(bboxes):
        cls1, x1, y1, x2, y2, conf1 = box1
        for j, box2 in enumerate(bboxes):
            if i != j:
                cls2, x1_, y1_, x2_, y2_, conf2 = box2
                if cls1 != cls2:
                    iou_value = iou((x1, y1, x2, y2), (x1_, y1_, x2_, y2_))
                    if iou_value > iou_threshold:
                        if (i, box1) not in overlapping_boxes:
                            overlapping_boxes[(i, box1)] = []
                        overlapping_boxes[(i, box1)].append((j, box2))
    return overlapping_boxes


# 选择conf最高的框
def select_highest_conf_boxes(bboxes, overlapping_boxes):
    indices_to_keep = set(range(len(bboxes)))
    for box1, overlapping in overlapping_boxes.items():
        _, box1_data = box1
        _, _, _, _, _, conf1 = box1_data
        for _, box2_data in overlapping:
            _, _, _, _, _, conf2 = box2_data
            if conf1 >= conf2:
                indices_to_keep.discard(box2_data)
            else:
                indices_to_keep.discard(box1_data)
    return [bboxes[i] for i in indices_to_keep]


# 选择conf最高的框，只筛选类别为1和2的框
def select_highest_conf_boxes(bboxes, overlapping_boxes, target_classes=(1, 2)):
    # 创建一个集合，包含所有检测框的索引，初始时假设所有框都要保留
    indices_to_keep = set(range(len(bboxes)))
    # 遍历每个重叠框组合
    for box1, overlapping in overlapping_boxes.items():
        # 获取第一个框的索引和数据
        index1, box1_data = box1
        cls1, _, _, _, _, conf1 = box1_data
        # 如果第一个框的类别不在目标类别中，则跳过
        if cls1 not in target_classes:
            continue
        # 遍历与第一个框重叠的其他框
        for index2, box2_data in overlapping:
            cls2, _, _, _, _, conf2 = box2_data
            # 如果第二个框的类别不在目标类别中，则跳过
            if cls2 not in target_classes:
                continue
            # 比较两个框的置信度，保留置信度较高的框的索引
            if conf1 >= conf2:
                # 移除置信度较低的框的索引
                indices_to_keep.discard(index2)
            else:
                # 移除置信度较低的框的索引
                indices_to_keep.discard(index1)
    # 返回保留下来的框
    return [bboxes[i] for i in indices_to_keep]


# 保存结果为yolo格式的txt文件
def save_yolo_txt(file_path, bboxes):
    with open(file_path, 'w') as f:
        for bbox in bboxes:
            cls, x1, y1, x2, y2, conf = bbox
            x_center = (x1 + x2) / 2
            y_center = (y1 + y2) / 2
            width = x2 - x1
            height = y2 - y1
            f.write(f"{cls} {x_center} {y_center} {width} {height} {conf}\n")

if __name__ == "__main__":
    configs = argparser()   # 加载参数配置
    detect_path = configs.detect_path
    new_detect_path = configs.new_detect_path

        # 先删除new_via_path下所有东西
    if os.path.exists(new_detect_path):
        shutil.rmtree(new_detect_path)
    else:
        os.makedirs(new_detect_path)
    
    for root, dirs, files in os.walk(detect_path):
        for file in files:
            if file.endswith('.txt'):
                txt_path = os.path.join(root, file)
                behavior_data = read_yolo_txt(txt_path)

                bboxes = convert_to_bbox(behavior_data)

                # 找到类别不同的重叠框
                overlapping_boxes = find_overlapping_boxes(bboxes)
                
                # 选择conf最高的框，只筛选类别为1和2的框
                final_bboxes = select_highest_conf_boxes(bboxes, overlapping_boxes, target_classes=(1, 2))

                # 构建新的文件路径
                relative_path = os.path.relpath(txt_path, detect_path)
                new_txt_path = os.path.join(new_detect_path, relative_path)

                # 确保新路径中的目录存在
                new_txt_dir = os.path.dirname(new_txt_path)

                
                if not os.path.exists(new_txt_dir):
                    os.makedirs(new_txt_dir)

                # 保存结果为yolo格式的txt文件
                save_yolo_txt(new_txt_path, final_bboxes)
