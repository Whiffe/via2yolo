# 这段代码是对举手的数据集进行via标注扩展，扩展更多动作
# python viaExtendAction1.py --Dataset_dir ./Dataset --newDataset_dir ./newDataset

import os
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--Dataset_dir', default='./Dataset',type=str)
parser.add_argument('--newDataset_dir', default='./newDataset',type=str)

arg = parser.parse_args()

# Dataset_dir 是举手数据集的位置
Dataset_dir = arg.Dataset_dir
# newDataset_dir 是扩展后的数据集的位置
newDataset_dir = arg.newDataset_dir

# 扩展数据集
attributes_dict = {
    '1': dict(aname='动作', type=3, options={'0': '举手', '1': '看书', '2': '写字', '3': '趴桌'}, default_option_id="",
              anchor_id='FILE1_Z0_XY1'),
    }

for root, dirs, files in os.walk(Dataset_dir, topdown=False):
    for name in files:
        if '.json' in name:
            json_path = os.path.join(root, name)
            with open(json_path) as f:
                json_data = json.load(f)
                # 添加扩展动作
                json_data['attribute'] = attributes_dict
                for ele in json_data['metadata']:
                    # 添加举手的标签
                    json_data['metadata'][ele]['av'] = {"1": "0"}
            new_json_pathx = json_path.replace(Dataset_dir, newDataset_dir)

            new_json = open(new_json_pathx, 'w')
            new_json.write(json.dumps(json_data))
