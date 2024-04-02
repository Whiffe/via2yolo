import os

def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.startswith("bb_"):
                new_filename = filename.replace("bb_", "")
                os.rename(os.path.join(root, filename), os.path.join(root, new_filename))
                continue
            if filename.endswith(".jpg") or filename.endswith(".txt"):
                # 获取文件名和扩展名
                name, ext = os.path.splitext(filename)
                # 根据文件名长度决定前缀0的个数
                prefix_zeros = "0" * (4 - len(name))
                # 新文件名
                new_filename = prefix_zeros + name + ext
                os.rename(os.path.join(root, filename), os.path.join(root, new_filename))

# 修改train文件夹下的文件名
rename_files("SCB-exetend-BUT2/images/train")
rename_files("SCB-exetend-BUT2/labels/train")

# 修改val文件夹下的文件名
rename_files("SCB-exetend-BUT2/images/val")
rename_files("SCB-exetend-BUT2/labels/val")
