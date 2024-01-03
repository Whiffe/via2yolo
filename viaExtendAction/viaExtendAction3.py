'''
viaExtendAction3.py 是将举手、看书、写字三个动作，扩展为三个模块的7个动作：

我们在标注过程中发现，举手与看书、写字可能同时存在，所以我们需要将举手单独放在一个模块。

【行为1：举手（raise the hand）】多选

【行为2：看书（read）、写字（write）、鼓掌（hand clap）、讨论（discuss）、趴桌（lie on the table）】单选

【行为3：说话（talk）】多选

python viaExtendAction3.py  --SCB3_via_Dataset ./SCB3_via_Dataset --SCB5_via_dataset ./SCB6_via_dataset
'''
import os
import json
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--SCB3_via_Dataset', default='./SCB3_via_Dataset',type=str)
parser.add_argument('--SCB5_via_dataset', default='./SCB5_via_dataset',type=str)

arg = parser.parse_args()

# SCB3_via_Dataset 是via SCB3数据集的位置
SCB3_via_Dataset = arg.SCB3_via_Dataset
# SCB5_via_dataset 是扩展后的via数据集的位置
SCB5_via_dataset = arg.SCB5_via_dataset

# 扩展数据集
attributes_dict =  {
		"1": {
			"aname": "behavior 1",
			"anchor_id": "FILE1_Z0_XY1",
			"type": 2,
			"desc": "",
			"options": {
				"0": "raise the hand",
			},
			"default_option_id": ""
		},
		"2": {
			"aname": "behavior 2",
			"anchor_id": "FILE1_Z0_XY1",
			"type": 2,
			"desc": "",
			"options": {
				"0": "read",
				"1": "write",
				"2": "hand clap",
				"3": "discuss",
				"4": "lie on the table"
			},
			"default_option_id": ""
		},
		"3": {
			"aname": "behavior 3",
			"anchor_id": "FILE1_Z0_XY1",
			"type": 2,
			"desc": "",
			"options": {
				"0": "talk",
			},
			"default_option_id": ""
		}
	}


# 清空 SCB5_via_dataset 下的文件及文件夹
if os.path.exists(SCB5_via_dataset):
    shutil.rmtree(SCB5_via_dataset)
# 将SCB3_via_dataset复制
shutil.copytree(SCB3_via_Dataset,SCB5_via_dataset)

for root, dirs, files in os.walk(SCB3_via_Dataset, topdown=False):
    for name in files:
        if '.json' in name:
            json_path = os.path.join(root, name)
            with open(json_path) as f:
                json_data = json.load(f)
                # 添加扩展动作
                json_data['attribute'] = attributes_dict
                # label_data_av = {}
                
                for ele in json_data['metadata']:
                    label_data_av = {}
                    pre_label_av = json_data['metadata'][ele]['av']['1']
                    # 判断是否有举手的动作
                    if '0' in pre_label_av:
                        label_data_av={"1":"0"}
                    # 判断是否有看书的动作
                    if '1' in pre_label_av:
                        label_data_av={"2":"0"}
                    # 判断是否有写字的动作
                    if '2' in pre_label_av:
                        label_data_av={"2":"1"}
                    json_data['metadata'][ele]['av'] = label_data_av
            new_json_pathx = json_path.replace(SCB3_via_Dataset, SCB5_via_dataset)
            
            new_json = open(new_json_pathx, 'w')
            new_json.write(json.dumps(json_data))
            
