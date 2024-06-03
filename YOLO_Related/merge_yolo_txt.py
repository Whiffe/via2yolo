'''
python merge_yolo_txt.py --folder1 ./SCB-yolo-TB/labels/52  --folder2 SCB-yolo-TB-detect2/52/labels/
python merge_yolo_txt.py --folder1 ./SCB-yolo-TB/labels/55  --folder2 SCB-yolo-TB-detect2/55/labels/
python merge_yolo_txt.py --folder1 ./SCB-yolo-TB/labels/57  --folder2 SCB-yolo-TB-detect2/57/labels/
python merge_yolo_txt.py --folder1 ./SCB-yolo-TB/labels/0081  --folder2 SCB-yolo-TB-detect2/0081/labels/
python merge_yolo_txt.py --folder1 ./SCB-yolo-TB/labels/0085  --folder2 SCB-yolo-TB-detect2/0085/labels/
python merge_yolo_txt.py --folder1 ./SCB-yolo-TB/labels/0086  --folder2 SCB-yolo-TB-detect2/0086/labels/
python merge_yolo_txt.py --folder1 ./SCB-yolo-TB/labels/0087  --folder2 SCB-yolo-TB-detect2/0087/labels/
python merge_yolo_txt.py --folder1 ./SCB-yolo-TB/labels/0088  --folder2 SCB-yolo-TB-detect2/0088/labels/
python merge_yolo_txt.py --folder1 ./SCB-yolo-TB/labels/0090  --folder2 SCB-yolo-TB-detect2/0090/labels/
python merge_yolo_txt.py --folder1 ./SCB-yolo-TB/labels/0091  --folder2 SCB-yolo-TB-detect2/0091/labels/


这个脚本会检查 folder2 中的所有 txt 文件，如果文件名在 folder1 中已经存在，则将 folder2 中对应文件的内容追加到 folder1 中的文件中。如果文件名不存在，则将文件从 folder2 复制到 folder1。
'''
import os
import shutil
import argparse


def argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--folder1', default='./folder1', type=str)
    parser.add_argument('--folder2', default='./folder2', type=str)

    return parser.parse_args()

def merge_folders(folder1, folder2):
    # 获取两个文件夹中的所有txt文件名
    folder1_files = {f for f in os.listdir(folder1) if f.endswith('.txt')}
    folder2_files = {f for f in os.listdir(folder2) if f.endswith('.txt')}
    
    # 创建目标文件夹，如果不存在
    if not os.path.exists(folder1):
        os.makedirs(folder1)
    
    # 遍历第二个文件夹中的txt文件
    for file in folder2_files:
        file_path2 = os.path.join(folder2, file)
        file_path1 = os.path.join(folder1, file)
        
        if file in folder1_files:
            # 如果文件名相同，追加内容
            with open(file_path2, 'r', encoding='utf-8') as f2, open(file_path1, 'a', encoding='utf-8') as f1:
                f1.write(f2.read())
        else:
            # 如果文件名不同，复制文件
            shutil.copy(file_path2, file_path1)

configs = argparser()   # 加载参数配置
# 示例文件夹路径
folder1 = configs.folder1
folder2 = configs.folder2

merge_folders(folder1, folder2)
