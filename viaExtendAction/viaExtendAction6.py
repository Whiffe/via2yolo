'''
viaExtendAction5.py 是将以下三个模块的动作（7个）扩展为四个模块的7+3个动作

raise the hand
read、write、hand clap、discuss、lie on the table
talk
guide、answer、On-stage interaction、blackboard-writing student、blackboard-writing teacher、make an inspection tour

扩展为：
raise the hand
read、write、hand clap、discuss、lie on the table
talk
guide、answer、On-stage interaction、blackboard-writing student、blackboard-writing teacher、make an inspection tour
bow the head,look up,turn the head

后续又将上述行为切换为中文：
举手
读、写、鼓掌、讨论、趴桌
说
指导、应答、台上互动、学生板书、教师板书、巡视
低,抬,转


python viaExtendAction6.py  --SCB_via_org ./SCB5-extend-tb2 --SCB_via_new ./SCB5-extend-stb
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
			"aname": "举手",
			"anchor_id": "FILE1_Z0_XY1",
			"type": 2,
			"desc": "",
			"options": {
				"0": "举手",
			},
			"default_option_id": ""
		},
		"2": {
			"aname": "课堂行为",
			"anchor_id": "FILE1_Z0_XY1",
			"type": 3,
			"desc": "",
			"options": {
				"0": "读",
				"1": "写",
				"2": "鼓掌",
				"3": "讨论",
				"4": "趴桌"
			},
			"default_option_id": ""
		},
		"3": {
			"aname": "说话",
			"anchor_id": "FILE1_Z0_XY1",
			"type": 2,
			"desc": "",
			"options": {
				"0": "说",
			},
			"default_option_id": ""
		},
		"4": {
			"aname": "教师行为",
			"anchor_id": "FILE1_Z0_XY1",
			"type": 3,
			"desc": "",
			"options": {
				"0": "指导",
				"1": "应答",
				"2": "台上互动",
				"3": "学生板书",
				"4": "教师板书",
				"5": "巡视",
			},
			"default_option_id": ""
		},
		"5": {
			"aname": "头部行为",
			"anchor_id": "FILE1_Z0_XY1",
			"type": 3,
			"desc": "",
			"options": {
				"0": "低",
				"1": "抬",
				"2": "转",
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
