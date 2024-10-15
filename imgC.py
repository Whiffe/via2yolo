'''
这个脚本用于比较两个文件夹中的图片文件前缀，检查 folder1 中的图片前缀是否都在 folder2 中存在，并列出缺失的前缀。

1 提取图片前缀：

从两个指定的文件夹路径（folder1 和 folder2）中遍历所有图片文件，提取每个图片文件的前缀。
如果图片文件名中包含下划线，则提取下划线前的部分作为前缀；如果没有下划线，则取文件名的前4位作为前缀。

2 比较前缀：

提取 folder1 和 folder2 中所有图片的前缀，分别存入两个集合 prefixes_folder1 和 prefixes_folder2。
比较两个文件夹中的前缀，查找 folder1 中的图片前缀是否在 folder2 中存在。
计算出 folder1 中存在但在 folder2 中缺失的前缀（即 missing_prefixes）。
打印结果：

3 打印 folder1 和 folder2 中提取的前缀集合。
打印缺失的前缀（missing_prefixes）。
如果没有缺失的前缀，打印提示所有前缀都存在；否则，列出哪些前缀在 folder2 中缺失。

'''
import os

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
    获取文件夹下所有图片的前缀，遍历所有子文件夹。
    """
    prefixes = set()
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                prefix = get_prefix(file)
                prefixes.add(prefix)
    return prefixes

def compare_prefixes(folder1, folder2):
    """
    比较两个文件夹中的图片前缀：
    检查folder1中的每个图片的前缀是否在folder2中存在
    """
    prefixes_folder1 = get_all_prefixes(folder1)
    prefixes_folder2 = get_all_prefixes(folder2)

    missing_prefixes = prefixes_folder1 - prefixes_folder2
    print("prefixes_folder1:",prefixes_folder1)
    print("prefixes_folder2:",prefixes_folder2)
    print("missing_prefixes:",missing_prefixes)
    print()

    return missing_prefixes

# 示例用法
# folder2 = "SCB5-Teacher-2024-9-17/images"
folder2 = "../SCB5/SCB5-BlackBoard-Sreen-Teacher-2024-10-15/images"
folder1 = "SCB5-BlackBoard-Sreen--2024-9-17/images"

missing = compare_prefixes(folder1, folder2)

if missing:
    print(f"以下前缀在 {folder2} 中缺失:")
    for prefix in missing:
        print(prefix)
else:
    print(f"{folder1} 中的所有图片前缀在 {folder2} 中都存在。")
