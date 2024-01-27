# 该脚本的作用是将 source_folder_path 路径下的每个文件夹下的视频 移动到 destination_folder_path 路径下，即把多个文件夹的视频移动到一个文件夹中
# python videos_all2one.py --source_folder_path ./videos --destination_folder_path ./01
import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--source_folder_path', default='./videos', type=str)
parser.add_argument('--destination_folder_path', default='./01', type=str)

arg = parser.parse_args()

source_folder_path = arg.source_folder_path
destination_folder_path = arg.destination_folder_path

def move_videos(source_folder, destination_folder):
    # 遍历源文件夹中的所有子文件夹
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            # 检查文件扩展名是否为视频格式，这里仅作示例，你可能需要根据实际情况添加更多的视频格式
            video_extensions = ['.mp4', '.avi', '.mkv', '.mov']
            if any(file.lower().endswith(ext) for ext in video_extensions):
                # 构建源文件的路径
                source_path = os.path.join(root, file)
                
                # 构建目标文件夹的路径
                destination_path = os.path.join(destination_folder, file)
                
                # 移动文件
                shutil.move(source_path, destination_path)
                print(f"移动 {file} 到 {destination_folder}")

# 输入源文件夹路径和目标文件夹路径
# source_folder_path = 'videos'
# destination_folder_path = '14'

# 调用函数
move_videos(source_folder_path, destination_folder_path)
