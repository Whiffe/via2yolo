'''
python imgcp.py
输入三个文件夹路径

第一个文件夹路径入SCB5-Teacher-2024-9-17/images/{train,val}/图片
然后提取出其中的图片前缀，如：
SCB5-BlackBoard-Sreen--2024-9-17/images/train/2_000214.jpg路径下，图片的前缀是2
SCB5-BlackBoard-Sreen--2024-9-17/images/train/149_002349.jpg路径下，图片的前缀是149

当然也有没有_的图片名字，没有_的图片名字，前缀就是前4位数字，入：
SCB5-BlackBoard-Sreen--2024-9-17/images/train/0001005.jpg，图片的前缀是0001

第二个文件夹路径：
提取的图片前缀就是第二个路径的文件夹名字，如下：
../via-classs-ST-2024-9-17/discuss/{0001,2,0002}

第三个文件夹路径：
我需要你利用第一个路径提取的图片前缀，找到第二个路径中图片前缀对应的文件夹，然后将这些文件夹复制到第三个文件夹路径中：../via-classs-ST-2024-9-17/BlackBoard-Sreen-Teacherw

简单来说：
提取第一个文件夹中所有图片的前缀。
在第二个文件夹中寻找与前缀对应的文件夹。
将这些对应的文件夹复制到指定的第三个文件夹路径中。

这个脚本通过提取图片前缀、匹配文件夹，并将文件夹复制到目标路径中，实现了将一组文件夹从源路径迁移到目标路径的功能。
'''

import os

import shutil

def get_prefix(file_name):
    """
    根据图片文件名提取前缀：
    1. 如果文件名包含下划线，则取下划线前的部分作为前缀。
    2. 如果文件名不包含下划线，则取文件名前4位作为前缀。
    """
    if '_' in file_name:
        return file_name.split('_')[0]
    else:
        return file_name[:4]

def get_all_prefixes(folder_path):
    """
    遍历文件夹，提取所有图片的前缀。
    """
    prefixes = set()  # 用集合存储前缀，避免重复
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                prefix = get_prefix(file)
                prefixes.add(prefix)
    return prefixes

def find_and_copy_folders(prefixes, src_folder, dest_folder):
    """
    根据前缀在第二个文件夹中寻找对应的子文件夹，并将这些子文件夹复制到第三个文件夹。
    """
    # 确保目标文件夹存在
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for prefix in prefixes:
        matching_folder = os.path.join(src_folder, prefix)
        if os.path.exists(matching_folder) and os.path.isdir(matching_folder):
            # 将文件夹复制到目标位置
            shutil.copytree(matching_folder, os.path.join(dest_folder, prefix))
            print(f"已复制文件夹: {matching_folder}")
        else:
            print(f"未找到匹配的文件夹: {matching_folder}")

def main(images_folder, src_prefix_folder, dest_folder):
    # 提取第一个文件夹下的所有图片前缀
    prefixes = get_all_prefixes(images_folder)

    # 找到前缀对应的文件夹并复制
    find_and_copy_folders(prefixes, src_prefix_folder, dest_folder)

# 示例用法
if __name__ == "__main__":
    images_folder = "SCB5-BlackBoard-Sreen--2024-9-17/images"
    src_prefix_folder = "../via-classs-ST-2024-9-17/discuss"
    dest_folder = "../via-classs-ST-2024-9-17/BlackBoard-Sreen-Teacher"
    
    main(images_folder, src_prefix_folder, dest_folder)
