# 计算yolo数据集中视频的数量，图片名中包含视频名信息
# python countVideos.py
import os

def count_videos(folder_path):
    video_count = []
    video_num = 0
    # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        # 遍历图片文件
        for file in files:
            if file.endswith('.jpg'):
                # 提取视频名
                video_name = file.split('_')[0]
                if video_name not in video_count:
                    video_count.append(video_name)
                    video_num = video_num + 1

    
    # 输出视频数量
    print("视频：\n",video_count)
    print("视频数量：",video_num)

# 测试代码
folder_path = './yolo_behavior_Dataset_all2/images/'
count_videos(folder_path)
