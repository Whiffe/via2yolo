# python yolo2via.py --img_path /root/autodl-tmp/1000 --label_path  ./runs/detect/1000/labels --json_path ./1000.json
from via3_tool import Via3Json
import os
import argparse
from collections import defaultdict
import cv2
import json

parser = argparse.ArgumentParser()
'''
--img_path 是图片的路径
--label_path 是yolo检测后txt的路径
--json_path 是将要生成json的路径
'''
parser.add_argument('--img_path', default='/root/autodl-tmp/1000',type=str)
parser.add_argument('--label_path', default='./runs/detect/1000/labels',type=str)
parser.add_argument('--json_path', default='./1000.json',type=str)

arg = parser.parse_args()

img_path = arg.img_path
json_path = arg.json_path
label_path = arg.label_path

#坐标格式转化 xywh代表：中心点与宽长，xyxy代表左上角点与右下角点
def xywh2xyxy(box):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    temp = box.copy()
    temp[0] = float(box[0]) - float(box[2]) / 2  # top left x
    temp[1] = float(box[1]) - float(box[3]) / 2  # top left y
    temp[2] = float(box[0]) + float(box[2]) / 2 # bottom right x
    temp[3] = float(box[1]) + float(box[3]) / 2  # bottom right y
    return temp

# 循环图片的数量，记录到num_images中
num_images = 0
for root, dirs, files in os.walk(img_path, topdown=False):
    for name in files:
        if '.png' in name:
            num_images += 1

via3 = Via3Json(json_path, mode='dump')
vid_list = list(map(str,range(1, num_images+1)))
via3.dumpPrejects(vid_list)
via3.dumpConfigs()

attributes_dict = {}

via3.dumpAttributes(attributes_dict)

files_dict,  metadatas_dict = {},{}

image_id = 1
for root, dirs, files in os.walk(img_path, topdown=False):
    files.sort()
    for name in files:
        if '.png' in name:
            files_dict[str(image_id)] = dict(fname=name, type=2)
            
            img = cv2.imread( os.path.join(root,name) ) #读取图片信息
            sp = img.shape #[高|宽|像素值由三种原色构成]
            img_H = sp[0]
            img_W = sp[1]
            
            txt_name = name.split('.png')[0]+'.txt'
            txt_path = os.path.join(label_path,txt_name)
            # 判断txt是否存在，因为未检测出目标的图片不会产生txt文件
            if os.path.exists(txt_path):
                print("txt_path:",txt_path)
                file_txt=open(txt_path).readlines()
                for vid,line in enumerate(file_txt,1):
                    array_line = line.split(' ')
                    yolo_box = [float(array_line[1]),float(array_line[2]),float(array_line[3]),float(array_line[4])]
                    via_box = xywh2xyxy(yolo_box)
                    metadata_dict = dict(vid=str(image_id),
                                    flg=str(0),
                                    xy=[2, float(via_box[0]*img_W), float(via_box[1]*img_H), float(via_box[2]*img_W)-float(via_box[0]*img_W), float(via_box[3])*img_H-float(via_box[1]*img_H)],
                                    av={'1': '0'})
                    metadatas_dict['image{}_{}'.format(image_id,vid)] = metadata_dict
             
        image_id += 1
            
    via3.dumpFiles(files_dict)
    via3.dumpMetedatas(metadatas_dict)

    views_dict = {}

    for i, vid in enumerate(vid_list,1):
        views_dict[vid] = defaultdict(list)
        views_dict[vid]['fid_list'].append(str(i))
    via3.dumpViews(views_dict)
    
    via3.dempJsonSave()
    
# 由于生成的json文件中存在 av={'1': '0'}，需要将其设置为 av={}，本来打算在生成的时候就这么写，但是报错
# 所以在生成之后替换掉

# 读取json
with open(json_path, 'r', encoding='utf-8') as f:
    json_file = f.read()
# 替换
json_file = json_file.replace("\"1\": \"0\"", " ")

# 保存json
json_out = json.loads(json_file)
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(json_out, f) 
