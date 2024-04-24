'''
视频名的命名：由4位数字组成，如0001、0002、0003、...、0028等
我输入一个视频文件夹的路径，把该文件夹的视频进行重命名
还要输出起始命名值，如0010，那么视频就是按照0010、0011的顺序重新命名，视频的格式是mp4或者mov

python video_rename.py --videos_path ./videos --video_start 35

'''
import os  
import shutil  
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--videos_path', type=str)
parser.add_argument('--video_start', type=int)

arg = parser.parse_args()
# 视频文件夹路径  
videos_path = arg.videos_path
# # 起始命名值，如这里为10，文件名将从0010开始  
video_start = arg.video_start
  
def rename_videos_in_folder(folder_path, start_value):  
    # 确保提供的路径存在且是文件夹  
    if not os.path.isdir(folder_path):  
        print(f"The provided path '{folder_path}' is not a valid directory.")  
        return  
      
    # 获取文件夹中所有文件的列表  
    files = os.listdir(folder_path)  
      
    # 过滤出mp4和mov文件  
    video_files = [f for f in files if f.lower().endswith(('.mp4', '.mov'))]  
      
    # 格式化起始命名值，确保它是4位数字  
    start_value_str = f"{start_value:04d}"  
      
    # 对每个视频文件进行重命名  
    for i, video_file in enumerate(video_files, start=start_value):  
        # 构建新的文件名  
        new_file_name = f"{i:04d}{os.path.splitext(video_file)[1]}"  
          
        # 构建原始文件路径和新文件路径  
        old_file_path = os.path.join(folder_path, video_file)  
        new_file_path = os.path.join(folder_path, new_file_name)  
          
        # 重命名文件  
        shutil.move(old_file_path, new_file_path)  
        print(f"Renamed '{old_file_path}' to '{new_file_path}'")  
  

rename_videos_in_folder(videos_path, video_start)
