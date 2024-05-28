'''
python yolo2via4.py --imgs_path SCB-via-TB --labels_path SCB-yolo-TB-detect --new_vias_path SCB-via-TB2

输入是第一个 img_path，是一个文件夹路径，这个文件夹有多个图片文件夹，如SCB-via-TB/{0081,0085,0086...}
输入的第二个是 yolo的检测结果 label_path

输出是多个图片文件所对应的json文件

就是将多个检测的文件夹转化为多个via的json文件
'''

from via3_tool2 import Via3Json
import os
import argparse
from collections import defaultdict
import cv2
import json
import shutil

def argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--imgs_path', default='./SCB-via-TB', type=str)
    parser.add_argument('--labels_path', default='./detect/', type=str)
    parser.add_argument('--new_vias_path',default='./SCB-via-TB2/', type=str)

    return parser.parse_args()


#坐标格式转化 xywh代表：中心点与宽长，xyxy代表左上角点与右下角点
def xywh2xyxy(box):
    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    temp = box.copy()
    temp[0] = float(box[0]) - float(box[2]) / 2  # top left x
    temp[1] = float(box[1]) - float(box[3]) / 2  # top left y
    temp[2] = float(box[0]) + float(box[2]) / 2 # bottom right x
    temp[3] = float(box[1]) + float(box[3]) / 2  # bottom right y
    return temp

def label2via(img_path,label_path, av_map):
    print("img_path:",img_path)
    image_id = 1
    files_dict,  metadatas_dict = {},{}
    for image_name in sorted(os.listdir(img_path)):
        if image_name.endswith(image_format):
            files_dict[str(image_id)] = dict(fname=image_name, type=2)
            img = cv2.imread( os.path.join(img_path,image_name) ) #读取图片信息
            sp = img.shape #[高|宽|像素值由三种原色构成]
            img_H = sp[0]
            img_W = sp[1]

            txt_name = image_name.split(image_format)[0]+'.txt'
            txt_path = os.path.join(label_path,txt_name)

            # 判断txt是否存在，因为未检测出目标的图片不会产生txt文件
            if os.path.exists(txt_path):
                # print("txt_path:",txt_path)
                file_txt=open(txt_path).readlines()
                
                for vid,line in enumerate(file_txt,1):
                    array_line = line.split(' ')
                    yolo_box = [float(array_line[1]),float(array_line[2]),float(array_line[3]),float(array_line[4])]
                    via_box = xywh2xyxy(yolo_box)
                    metadata_dict = dict(
                        vid=str(image_id),
                        xy=[
                            2, 
                            float(via_box[0]*img_W), 
                            float(via_box[1]*img_H), 
                            float(via_box[2]*img_W)-float(via_box[0]*img_W), 
                            float(via_box[3])*img_H-float(via_box[1]*img_H)
                        ],
                        av=av_map[array_line[0]]
                    )
                    metadatas_dict['image{}_{}'.format(image_id,vid)] = metadata_dict
        else:
            continue    
        image_id += 1
    return files_dict, metadatas_dict  

if __name__ == '__main__':
    configs = argparser()   # 加载参数配置

    imgs_path = configs.imgs_path
    labels_path = configs.labels_path
    new_vias_path = configs.new_vias_path

    image_format = '.jpg'


    # 先删除new_via_path下所有东西
    if os.path.exists(new_vias_path):
        shutil.rmtree(new_vias_path)
    else:
        os.makedirs(new_vias_path)


    '''
    av_map 需要根据需求修改

    检测结果有啥就咋修改

    "0":{"1": "0"},
    代表 av中第一类行为 举手 行为的映射

    "1":{"2": "0"},
    代表 av中第二类行为 看书 行为的映射

    "1":{"2": "1"},
    代表 av中第二类行为 写字 行为的映射

    '''

    av_map = {
        "0":{"1": "0"},
        "1":{"2": "0"},
        "2":{"2": "1"},
    }


    '''
    type=3 是多选，type=2 是单选
    '''
    attributes_dict = {
        "1":dict(
            aname="behavior 1",
            anchor_id = 'FILE1_Z0_XY1',
            type=2,
            desc="",
            options={
                "0":"raise the hand"
            },
            default_option_id=""
        ),
        "2":dict(
            aname="behavior 2",
            anchor_id = 'FILE1_Z0_XY1',
            type=3,
            desc="",
            options={
                "0":"read",
                "1":"write",
                "2":"hand clap",
                "3":"discuss",
                "4":"lie on the table",
            },
            default_option_id=""
        ),
        "3":dict(
            aname="behavior 3",
            anchor_id = 'FILE1_Z0_XY1',
            type=2,
            desc="",
            options={
                "0":"talk"
            },
            default_option_id=""
        ),
        "4":dict(
            aname="behavior 4",
            anchor_id = 'FILE1_Z0_XY1',
            type=3,
            desc="",
            options={
                "0":"guide",
                "1":"answer",
                "2":"On-stage interaction",
                "3":"blackboard-writing student",
                "4":"blackboard-writing teacher",
                "5":"make an inspection tour",
            },
            default_option_id=""
        ),
    }

    # 遍历 img_path 文件夹
    for img_folder_name in os.listdir(imgs_path):
        if 'DS_Store' in img_folder_name:
            continue
        if 'init.json' in img_folder_name:
            continue
        img_path = os.path.join(imgs_path, img_folder_name)
        label_path = os.path.join(labels_path, img_folder_name, 'labels')
        new_via_path = os.path.join(new_vias_path, img_folder_name)

        os.makedirs(new_via_path)

        # 循环图片的数量，记录到num_images中
        num_images = 0
        
        for image_name in os.listdir(img_path):
            if image_name.endswith(image_format):
                num_images += 1
                image_file_path = os.path.join(img_path, image_name)
                # 复制 image_file_path 到 new_via_path
                shutil.copy(image_file_path, new_via_path)
                
        json_path = os.path.join(new_via_path, f"{img_folder_name}.json")

        via3 = Via3Json(json_path, mode='dump')
        vid_list = list(map(str,range(1, num_images+1)))
        via3.dumpPrejects(vid_list)
        via3.dumpConfigs()

        via3.dumpAttributes(attributes_dict)

        files_dict, metadatas_dict = label2via(img_path,label_path, av_map)
        
        via3.dumpFiles(files_dict)
        via3.dumpMetedatas(metadatas_dict)

        views_dict = {}

        for i, vid in enumerate(vid_list,1):
            views_dict[vid] = defaultdict(list)
            views_dict[vid]['fid_list'].append(str(i))
        via3.dumpViews(views_dict)
        
        via3.dempJsonSave()

