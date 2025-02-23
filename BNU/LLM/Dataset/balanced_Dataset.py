'''
python balanced_Dataset.py --input_dir ./result.json --out_dir ./balanced_result.json

balanced_Dataset.py
数据平衡操作：将超过平均数的类别，进行采样，让其类别数量等于平均数
'''
import json
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default='./result.json')
parser.add_argument('--out_dir', type=str, default='./balanced_result.json')
arg = parser.parse_args()

# 读取 JSON 文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 统计每个类别的数量，并获取所有类别
def count_categories(data):
    category_count = {}
    for item in data:
        for message in item["messages"]:
            if message["role"] == "assistant":
                category = message["content"]
                if category in category_count:
                    category_count[category] += 1
                else:
                    category_count[category] = 1
    return category_count

# 计算类别的平均数量
def calculate_average_count(category_count):
    total_count = sum(category_count.values())
    num_categories = len(category_count)
    if num_categories == 0:
        return 0
    return total_count / num_categories

# 对超过平均数的类别进行采样
def sample_categories(data, category_count, average_count):
    category_items = {category: [] for category in category_count}
    for index, item in enumerate(data):
        for message in item["messages"]:
            if message["role"] == "assistant":
                category = message["content"]
                category_items[category].append(index)

    selected_indices = []
    for category, count in category_count.items():
        if count > average_count:
            selected_indices.extend(random.sample(category_items[category], int(average_count)))
        else:
            selected_indices.extend(category_items[category])

    selected_indices.sort()
    new_data = [data[i] for i in selected_indices]
    return new_data

# 保存处理后的 JSON 文件
def save_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 主函数
def main():
    input_file = arg.input_dir  # 输入的 JSON 文件路径
    output_file = arg.out_dir  # 输出的 JSON 文件路径

    # 读取 JSON 文件
    data = read_json_file(input_file)

    # 统计处理前每个类别的数量，并获取所有类别
    pre_balance_category_count = count_categories(data)
    # print("平衡数据处理前每个类别的数量:", pre_balance_category_count)
    print("平衡数据处理前每个类别的数量:")
    # print("类别的平均数量:", average_count)
    for category, count in pre_balance_category_count.items():
        print(f"{category}: {count}")
    print("---------")

    # 计算类别的平均数量
    average_count = calculate_average_count(pre_balance_category_count)
    # 对超过平均数的类别进行采样
    new_data = sample_categories(data, pre_balance_category_count, average_count)

    # 统计处理后每个类别的数量
    post_balance_category_count = count_categories(new_data)
    # print("平衡数据处理后每个类别的数量:", post_balance_category_count)
    print("平衡数据处理后每个类别的数量:")
    for category, count in post_balance_category_count.items():
        print(f"{category}: {count}")

    # 保存处理后的 JSON 文件
    save_json_file(new_data, output_file)
    print("处理后的 JSON 文件已保存到:", output_file)

if __name__ == "__main__":
    main()
