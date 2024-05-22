'''
viaExtendAction5.py 是将以下三个模块的动作（7个）扩展为四个模块的7+3个动作

raise the hand
read、write、hand clap、discuss、lie on the table
talk

扩展为：
raise the hand
read、write、hand clap、discuss、lie on the table
talk
guide、answer、On-stage interaction、blackboard-writing student、blackboard-writing teacher、make an inspection tour

python viaExtendAction5.py  --SCB_via_org ./SCB5-extend-tb --SCB_via_new ./SCB5-extend-tb2
'''
import os
import json
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--SCB_via_org', default='./SCB_via_org',type=str)
parser.add_argument('--SCB_via_new', default='./SCB_via_new',type=str)

arg = parser.parse_args()

# SCB_via_org 是via SCB3数据集的位置
SCB_via_org = arg.SCB_via_org
# SCB_via_new 是扩展后的via数据集的位置
SCB_via_new = arg.SCB_via_new

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
			"type": 3,
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
		},
		"4": {
			"aname": "behavior 4",
			"anchor_id": "FILE1_Z0_XY1",
			"type": 3,
			"desc": "",
			"options": {
				"0": "guide",
				"1": "answer",
				"2": "On-stage interaction",
				"3": "blackboard-writing student",
				"4": "blackboard-writing teacher",
				"5": "make an inspection tour",
			},
			"default_option_id": ""
		}
	}


# 清空 SCB_via_new 下的文件及文件夹
if os.path.exists(SCB_via_new):
    shutil.rmtree(SCB_via_new)
# 将SCB_via_org复制
shutil.copytree(SCB_via_org,SCB_via_new)

for root, dirs, files in os.walk(SCB_via_org, topdown=False):
    for name in files:
        if '.json' in name:
            json_path = os.path.join(root, name)
            print("json_path:",json_path)
            with open(json_path) as f:
                json_data = json.load(f)
                # 添加扩展动作
                json_data['attribute'] = attributes_dict
                
            new_json_pathx = json_path.replace(SCB_via_org, SCB_via_new)
            
            new_json = open(new_json_pathx, 'w')
            new_json.write(json.dumps(json_data))
