import os  
  
# 设置图片和标签文件夹的路径  
images_folder = 'moon-images-12-8'  
labels_folder = 'moon-labels-12-8'  
  
# 确保标签文件夹存在  
if not os.path.exists(labels_folder):  
    os.makedirs(labels_folder)  
  
# 遍历图片文件夹中的所有jpg文件  
for filename in os.listdir(images_folder):  
    if filename.endswith('.jpg'):  
        # 提取图片文件名（不含扩展名）  
        base_filename = os.path.splitext(filename)[0]  
          
        # 格式化文件名以匹配所需的txt文件名（如果需要特定的格式，可以在这里调整）  
        txt_filename = base_filename + '.txt'  
          
        # 构建完整的txt文件路径  
        txt_file_path = os.path.join(labels_folder, txt_filename)  
          
        # 创建空的txt文件  
        with open(txt_file_path, 'w') as f:  
            pass  # 不需要写入任何内容，因为文件默认就是空的  
          
        print(f"Created empty txt file for {filename}: {txt_file_path}")