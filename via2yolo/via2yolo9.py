'''
这一段代码是将via转化为yolo格式，修正了via2yolo8不能按照视频文件/json文件分割训练测试集的问题

python via2yolo9.py --via_Dataset  ./via-classs-ST-2024-6-13/ --yolo_Dataset ./yolo-classs-ST-2024-6-13 --tain_r 0.8 --behavior_av_ids 5

注意这是 via 中多个动作转化为yolo格式
并且可以检查没有标注的框（或者小点），并给出没有标注的图片

这个脚本是对下面格式via数据进行提取的
av 1 : raise the hand
av 2 : read、write、hand clap、discuss、lie on the table
av 3 : talk
av 4 : guide、answer、On-stage interaction、blackboard-writing student、blackboard-writing teacher、make an inspection tour

这一部分是从via2yolo4.py修改的，主要改动是可以提取对应av的行为

比如只要av 1 中的 raise the hand，只需要  --behavior_av_id 1

0  举手 hand-raising
1  阅读 read
2  写 write
3  讨论 discuss
4  说话 talk
5  低头 bow the head
6  抬头 look up
7  转头 turn the head
8  指导 guide
9  应答 answer
10 台上互动 On-stage interaction
11 学生板书 blackboard-writing student
12 教师板书 blackboard-writing teacher
13 巡视 make an inspection tour


av 1 : raise the hand
raise the hand 0 -> hand-raising 0

av 2 : read、write、hand clap、discuss、lie on the table
read 0 -> read 1 
write 1 -> write 2


{
    "1":[
        {"0":"0"}
    ],
    "2":[
        {"0":"1"},
        {"1":"2"}
    ]
}

{
    "1":[
        {"0":"0"}
    ],
    "2":[
        {"0":"1"},
        {"1":"2"}
    ],
    "4":[
        {"0":"3"},
        {"1":"4"},
        {"2":"5"},
        {"3":"6"}
    ]
}


    b_map = {
        "1":{
            "0":"0"
        },
        "2":{
            "0":"1",
            "1":"1"
        },
        "4":{
            "0":"3",
            "1":"4"
        }
    }

    b_map = {
        "1":{
            "0":"0"
        },
        "2":{
            "0":"1",
            "1":"1"
        },
        "4":{
            "0":"3",
            "1":"4",
            "2":"5",
            "3":"6"
        }
    }
'''

import os
import json
import cv2
import random
import argparse
import shutil


def argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--via_Dataset', default='./via_Dataset', type=str)
    parser.add_argument('--yolo_Dataset', default='./yolo_Dataset', type=str)
    parser.add_argument('--tain_r', default=0.8, type=float)
    parser.add_argument('--behavior_av_ids', default=3, type=int)

    return parser.parse_args()



def get_action_id(behavior_av_id, av, image_name, xywh):
    action_id = -1
    # 获取动作的id
    # 先判断 当前的候选框中有没有behavior_av_id，如果有就保存action_id
    if behavior_av_id in av.keys() and behavior_av_id in b_map:
        try:
            # 获取当前av对应的行为ID：action_temp_id
            action_temp_id = av[behavior_av_id]
            # 将 action_temp_id 通过 b_map 映射到目标行为ID
            # 先判断 action_temp_id 是否在所需要的映射范围内
            if action_temp_id in b_map[behavior_av_id].keys():
                action_id = b_map[behavior_av_id][action_temp_id]
        except KeyError:
            print("KeyError:",KeyError)
            print("av:",av)
            print("下面的图片中有没有标注的框")
            print(f"image_name: {image_name}, xywh: {xywh}")
    else:
        if len(av) == 0:
            print("len(av):",len(av))
            print("av:",av)
            print("下面的图片中 出现av为空的情况 {}")
            print(f"image_name: {image_name}, xywh: {xywh}")
    return action_id

# via2yolo 函数是将via信息转化为yolo的格式·
def via2yolo(json, root, train_val):
    # 循环读出每一个框的信息
    for i in json['metadata']:
        # 从 i 中获取 vid
        vid = i.split('_')[0]
        if 'image' in vid:
            vid = vid.split('image')[-1]
        # 获取对应的图片名字
        image_name = json['file'][vid]['fname']
        # print("image_name",image_name)
        
        # 获取图片的路径
        # 由于图片是一个链接，所以就取链接的最后一个 / 后面的内容
        image_dir = os.path.join(root, image_name.split('/')[-1])


        # 读取图片的高和宽
        img = cv2.imread(image_dir)
        h = img.shape[0]
        w = img.shape[1]

        # 读取 via 中的 坐标 xywh，框的左上角坐标 x y，与框的宽高
        xywh = json['metadata'][i]['xy'][1:]

        av = json['metadata'][i]['av']
        
        # 遍历behavior_av_ids，即把所有av遍历一遍
        # 这样遍历，会让一个n种行为的目标，有n行相同的坐标，但是每行相同坐标的行为ID不同
        for behavior_av_id in range(behavior_av_ids):
            behavior_av_id = str(behavior_av_id + 1)

            action_id = get_action_id(behavior_av_id, av, image_name, xywh)

            if action_id == -1:
                # print("action_id 未获取，图片：",image_name)
                continue
            '''
            将xywh 转化为 yolo 的格式
            第一个参数是0，代表举手这一个分类
            第二个参数是，框的中心坐标 x，归一化处理
            第三个参数是，框的中心坐标 y，归一化处理
            第四个参数是，框的宽度 w，归一化处理
            第五个参数是，框的高度 h，归一化处理
            第六个参数是，换行
            '''
            xcyc_wh = action_id + ' ' + str((xywh[0] + xywh[2] / 2) / w) + ' ' + str((xywh[1] + xywh[3] / 2) / h) + \
                    ' ' + str(xywh[2] / w) + ' ' + str(xywh[3] / h) + '\n'

            # 设置 txt 的 train 和 val 的路径
            # image_name 是一个链接，所以需要做提取
            temp_train_txt_path = os.path.join(train_label_dir, image_name.split('/')[-1].split('.')[0] + '.txt')
            temp_val_txt_path = os.path.join(val_label_dir, image_name.split('/')[-1].split('.')[0] + '.txt')

            '''
            判断当前的 temp_train_txt_path 或者 temp_val_txt_path 是否已经存在
            如果不存在，就进入 if 中
            不存在代表已经进入下一个图片的框了，需要创建一个新的txt
            如果存在，就进入 else 中
            '''
            if not (os.path.isfile(temp_train_txt_path) or os.path.isfile(temp_val_txt_path)):
                # 这里的 train 和 val 的划分 采用随机数方式
                # 这里会更新 txt 的路径 和图片 的路径
                # 由于图片是一个链接，所以就取链接的最后一个 / 后面的内容
                if train_val:
                    txt_path = temp_train_txt_path
                    image_path = os.path.join(train_image_dir, image_name.split('/')[-1])
                else:
                    txt_path = temp_val_txt_path
                    image_path = os.path.join(val_image_dir, image_name.split('/')[-1])
                # 将图片复制到指定路径
                shutil.copy(image_dir,image_path)
                '''
                由于via中的标注可能存在后续的添加的框，使得框的顺序会是乱的
                如果不加下放的 else 内容，会使得后续的添加的框不能放在对应的txt中，而放到了上一个循环的txt中
                所以需要在 else 中判断，当前循环的框所对应的图片名与当前的txt名是否相同，如果不同，说明出现上述问题
                那么就需要重置txt
            '''
            else:
                # 判断 当前循环的框所对应的图片名与当前的 txt 名是否相同
                if image_name.split('.')[0] == image_name.split('/')[-1].split('.')[0]:
                    # 判断 重置的 txt 路径是在 train 中还是在 val 中
                    if os.path.isfile(temp_train_txt_path):
                        txt_path = temp_train_txt_path
                    else:
                        txt_path = temp_val_txt_path
            # 向指定txt路径追加内容
            with open(txt_path, "a") as file:  # a，代表追加内容
                file.write(xcyc_wh)

if __name__ == '__main__':
    configs = argparser()   # 加载参数配置

    via_Dataset = configs.via_Dataset

    # yolo数据集的存放位置 Dataset_dir
    yolo_Dataset = configs.yolo_Dataset

    # behavior_av_ids 代表总共有多少种大类
    behavior_av_ids = configs.behavior_av_ids

    # b_map 需要根据需求修改
    '''
    b_map = {
        "1":{
            "0":"0"
        },
        "2":{
            "0":"1",
            "1":"2"
        }
    }
    b_map = {
        "1":{
            "0":"0"
        },
        "2":{
            "0":"1",
            "1":"1"
            }
    }
    '''

    b_map = {
        "1":{
            "0":"0"
        },
        "2":{
            "0":"1",
            "1":"1"
        },
        "4":{
            "0":"3",
            "1":"4"
        }
    }

    # 删除 Dataset_dir 文件夹
    if os.path.exists(yolo_Dataset):
        shutil.rmtree(yolo_Dataset)
    # 在 Dataset_dir 下创建 labels images train val
    os.makedirs(yolo_Dataset + '/labels/train')
    os.makedirs(yolo_Dataset + '/labels/val')
    os.makedirs(yolo_Dataset + '/images/train')
    os.makedirs(yolo_Dataset + '/images/val')


    # 训练集与验证集的比例，tain_r代表训练集的比例，1-tain_r 代表验证集的比例
    tain_r = configs.tain_r
    # 设置 labels images train val 的路径
    train_label_dir = yolo_Dataset + '/labels/train/'
    val_label_dir = yolo_Dataset + '/labels/val/'
    train_image_dir = yolo_Dataset + '/images/train/'
    val_image_dir = yolo_Dataset + '/images/val/'

    # 循环 读出所有json文件
    for root, dirs, files in os.walk(via_Dataset, topdown=False):
        files.sort()
        for name in files:
            file_dir = os.path.join(root, name)
            if '.json' in name:
                print(file_dir)
                train_val = False # Fasle代表val， True代表train
                if random.random() <= tain_r:
                    train_val = True
                
                try:
                    file_json = open(file_dir, 'r')
                    file_json_content = json.loads(file_json.read())
                except:
                    file_json = open(file_dir, 'r', encoding='gb18030', errors='ignore')
                    file_json_content = json.loads(file_json.read())
                    
                via2yolo(file_json_content, root, train_val)
                file_json.close()
                print(file_dir)
