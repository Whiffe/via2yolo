import os
import json
import shutil

def process_json(json_path, src_base_dir, target_base_dir):
    # 读取JSON文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 收集所有分类标签
    categories = set()
    for entry in data:
        for msg in entry["messages"]:
            if msg["role"] == "assistant":
                categories.add(msg["content"])
                break  # 每个entry只取第一个assistant的content
    
    # 创建/清空目标文件夹
    for category in categories:
        category_dir = os.path.join(target_base_dir, category)
        # 清空已存在文件夹
        if os.path.exists(category_dir):
            shutil.rmtree(category_dir)
        os.makedirs(category_dir, exist_ok=True)
    
    # 复制图片到对应目录
    for entry in data:
        # 获取分类标签
        category = None
        for msg in entry["messages"]:
            if msg["role"] == "assistant":
                category = msg["content"]
                break
        
        if not category:
            continue
        
        # 处理所有图片
        for img_rel_path in entry["images"]:
            src_path = os.path.join(src_base_dir, img_rel_path)
            dest_dir = os.path.join(target_base_dir, category)
            
            # 确保源文件存在
            if not os.path.exists(src_path):
                print(f"警告：文件不存在 {src_path}")
                continue
            
            # 执行复制
            try:
                shutil.copy(src_path, dest_dir)
                print(f"已复制 {img_rel_path} -> {dest_dir}")
            except Exception as e:
                print(f"复制失败 {src_path}: {str(e)}")

if __name__ == "__main__":
    # 配置路径（根据实际情况修改）
    json_file = "Bridge_Behavior.json"          # JSON文件路径
    source_base = "."                # 图片源文件基础目录
    target_base = "classified_images" # 分类存储目标目录
    
    # 执行处理
    process_json(json_file, source_base, target_base)