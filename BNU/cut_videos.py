'''
conda install x264 ffmpeg -c conda-forge -y

conda install -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ x264 ffmpeg -y
'''
# python cut_videos.py --IN_DATA_DIR videos_flotage_06 --OUT_DATA_DIR frames_flotage_06 --FRAME_RATE 1
# python cut_videos.py --IN_DATA_DIR videos --OUT_DATA_DIR frames --FRAME_RATE 1
# 将一个视频文件夹的视频抽帧
import os  
import shutil  
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--IN_DATA_DIR', type=str)
parser.add_argument('--OUT_DATA_DIR', type=str)
parser.add_argument('--FRAME_RATE', type=int, default=1)

arg = parser.parse_args()
IN_DATA_DIR = arg.IN_DATA_DIR
OUT_DATA_DIR = arg.OUT_DATA_DIR
FRAME_RATE = arg.FRAME_RATE # 这里假定帧率为1，您可以根据需要修改  

def convert_videos_to_frames(in_data_dir, out_data_dir, frame_rate):  
    # 检查输出目录是否存在，如果不存在则创建  
    if not os.path.exists(out_data_dir):  
        os.makedirs(out_data_dir)  
      
    # 遍历输入目录中的所有文件  
    for video_path in os.listdir(in_data_dir):  
        video_path = os.path.join(in_data_dir, video_path)  
          
        # 获取视频文件名（不含路径）  
        video_name = os.path.basename(video_path)  
          
        # 根据视频文件扩展名去除后缀  
        if video_name.endswith('.webm'):  
            video_name = video_name[:-5]  
        else:  
            video_name = video_name[:-4]  
          
        # 构建输出目录路径  
        out_video_dir = os.path.join(out_data_dir, video_name)  
          
        # 创建输出目录  
        if not os.path.exists(out_video_dir):  
            os.makedirs(out_video_dir)  
          
        # 构建输出文件名模板  
        out_name = os.path.join(out_video_dir, f"{video_name}_%06d.jpg")  
          
        # 使用ffmpeg命令将视频转换为帧  
        command = [  
            'ffmpeg',  
            '-i', video_path,  
            '-r', str(frame_rate),  
            '-q:v', '1',  
            out_name  
        ]  
        subprocess.run(command, check=True)  
  
convert_videos_to_frames(IN_DATA_DIR, OUT_DATA_DIR, FRAME_RATE)
