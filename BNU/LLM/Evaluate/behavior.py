from QwenModel import load_model, get_model_output
from qwen_vl_utils import process_vision_info
import argparse
from tqdm import tqdm
import os
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompt', default='./prompt/bridge_behavior.txt', type=str)
    parser.add_argument('--dataset', default='./experimental_Bridge/', type=str)
    parser.add_argument('--output', default='./output/result.txt', type=str)
    parser.add_argument('--model_path', default="/root/Qwen/Qwen2-VL-7B-Instruct-2", type=str)
    return parser.parse_args()

def process():
    configs = argparser()

    # 加载模型
    model, processor = load_model(configs.model_path)

    def read_txt(txt_path):
        with open(txt_path, "r") as f:
            return f.read()

    prompt = read_txt(configs.prompt)
    # 初始化变量
    all_true_labels = []  # 存储所有真实标签
    all_predicted_labels = []  # 存储所有预测标签

    # 获取所有子目录
    subdirs = [d for d in os.listdir(configs.dataset) if os.path.isdir(os.path.join(configs.dataset, d))]

    # 遍历每个子目录
    for subdir in tqdm(subdirs, desc="Processing subdirectories"):
        subdir_path = os.path.join(configs.dataset, subdir)
        excel_file = f"{subdir}_behavior.xlsx"  # 构造Excel文件名
        excel_path = os.path.join(subdir_path, excel_file)

        # 检查Excel文件是否存在
        if not os.path.exists(excel_path):
            print(f"Skipping {subdir} due to missing {excel_file}")
            continue

        # 读取Excel文件
        data = pd.read_excel(excel_path, header=None)

        # 遍历Excel文件中的每一行
        for _, row in data.iterrows():
            image_name = row[0]
            if not isinstance(image_name, str):
                continue  # Skip invalid entries
            image_path = os.path.join(subdir_path, f"{image_name}.jpg")
            if not os.path.exists(image_path):
                continue  # Skip if the image doesn't exist

            # 提取真实标签
            label_mapping = {0: "测距离", 1: "放板子", 2: "放重物", 3: "称重物", 4: "记数据"}
            ground_truth = []
            for i in range(1, len(row)):
                if pd.notna(row[i]) and row[i] in label_mapping:
                    ground_truth.append(label_mapping[row[i]])

            # 获取模型输出
            result = get_model_output(prompt, image_path, model, processor)
            output_text = result.strip()

            # Process output
            predicted_labels = {output_text.strip()}  # 模型输出为单个标签
            true_labels = set(ground_truth)

            # 处理 true_labels 为空的情况
            if len(true_labels) == 0:
                # 如果 true_labels 为空，认为预测标签是正确的
                true_labels = {'其他'}

            # Debugging output
            print("image_path:", image_path)
            print("predicted_labels:", predicted_labels)
            print("true_labels:", true_labels)

            # 将当前样本的真实标签和预测标签添加到汇总列表中
            all_true_labels.append(true_labels)
            all_predicted_labels.append(predicted_labels)

    # 计算总体指标
    # 将标签转换为多标签格式
    all_labels = set([label for sublist in all_true_labels for label in sublist] + 
                     [label for sublist in all_predicted_labels for label in sublist])
    label_to_index = {label: idx for idx, label in enumerate(all_labels)}

    y_true = [[1 if label in true_labels or len(true_labels) == 0 else 0 for label in all_labels] for true_labels in all_true_labels]
    y_pred = [[1 if label in pred_labels else 0 for label in all_labels] for pred_labels in all_predicted_labels]

    print("----Overall Metrics--------")
    overall_precision = precision_score(y_true, y_pred, average="micro")
    overall_recall = recall_score(y_true, y_pred, average="micro")
    overall_f1 = f1_score(y_true, y_pred, average="micro")
    print(f"Overall Precision: {overall_precision}")
    print(f"Overall Recall: {overall_recall}")
    print(f"Overall F1 Score: {overall_f1}")

if __name__ == "__main__":
    process()
