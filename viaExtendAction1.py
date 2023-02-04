# 这段代码是对举手的数据集进行via标注扩展，扩展更多动作
# python viaExtendAction1.py --riseHand_via_dataset ./riseHand_via_dataset --RRW_via_Dataset ./RRW_via_Dataset

import os
import json
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--riseHand_via_dataset', default='./riseHand_via_dataset',type=str)
parser.add_argument('--RRW_via_Dataset', default='./RRW_via_Dataset',type=str)

arg = parser.parse_args()

# Dataset_dir 是via举手数据集的位置
riseHand_via_dataset = arg.riseHand_via_dataset
# newDataset_dir 是扩展后的via数据集的位置，RRW分别代表举手、看书、写字
RRW_via_Dataset = arg.RRW_via_Dataset

# 扩展数据集
attributes_dict = {
    '1': dict(aname='动作', type=3, options={'0': '举手', '1': '看书', '2': '写字', '3': '趴桌'}, default_option_id="",
              anchor_id='FILE1_Z0_XY1'),
    }

# 清空 RRW_via_Dataset 下的文件及文件夹
if os.path.exists(RRW_via_Dataset):
    shutil.rmtree(RRW_via_Dataset)
# 将riseHand_via_dataset复制
shutil.copytree(riseHand_via_dataset,RRW_via_Dataset)

for root, dirs, files in os.walk(riseHand_via_dataset, topdown=False):
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
            new_json_pathx = json_path.replace(riseHand_via_dataset, RRW_via_Dataset)

            new_json = open(new_json_pathx, 'w')
            new_json.write(json.dumps(json_data))
