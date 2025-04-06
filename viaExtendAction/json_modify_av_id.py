'''
python 1.py  via-classs-ST-2025-03-25  via1111

以下文件发生了替换:
文件: via1111/0002/0002.json
对应的 vid 值: 27
文件: via1111/0100/0100.json
对应的 vid 值: 83, 82, 81, 79
文件: via1111/1322/1322.json
对应的 vid 值: 18
文件: via1111/0001/0001.json
对应的 vid 值: 61, 58, 58
文件: via1111/1307/1307.json
对应的 vid 值: 11, 12, 13
'''
import os
import json
import shutil
import argparse


def modify_json(json_data):
    modified = False
    modified_vids = []
    if 'metadata' in json_data:
        for key in json_data['metadata']:
            av = json_data['metadata'][key].get('av')
            if av and '2' in av:
                if av['2'] == '6':
                    json_data['metadata'][key]['av'] = {'3': '1'}
                    modified = True
                    modified_vids.append(json_data['metadata'][key]['vid'])
                elif av['2'] == '7':
                    json_data['metadata'][key]['av'] = {'3': '2'}
                    modified = True
                    modified_vids.append(json_data['metadata'][key]['vid'])
    return json_data, modified, modified_vids


def process_folder(input_folder, output_folder):
    modified_files = []
    modified_vids_per_file = {}
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for root, dirs, files in os.walk(input_folder):
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)
        for file in files:
            input_file_path = os.path.join(root, file)
            output_file_path = os.path.join(output_subfolder, file)
            if file.endswith('.json'):
                try:
                    with open(input_file_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)
                    new_json_data, modified, modified_vids = modify_json(json_data)
                    if modified:
                        modified_files.append(output_file_path)
                        modified_vids_per_file[output_file_path] = modified_vids
                        with open(output_file_path, 'w', encoding='utf-8') as f:
                            json.dump(new_json_data, f, indent=4)
                    else:
                        shutil.copy2(input_file_path, output_file_path)
                except Exception as e:
                    print(f"处理文件 {input_file_path} 时出错: {e}")
            else:
                shutil.copy2(input_file_path, output_file_path)
    return modified_files, modified_vids_per_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='修改 JSON 文件中的 av 字段')
    parser.add_argument('input_folder', type=str, help='输入文件夹路径')
    parser.add_argument('output_folder', type=str, help='输出文件夹路径')
    args = parser.parse_args()
    input_folder = args.input_folder
    output_folder = args.output_folder
    modified_files, modified_vids_per_file = process_folder(input_folder, output_folder)
    if modified_files:
        print("以下文件发生了替换:")
        for file in modified_files:
            print(f"文件: {file}")
            print(f"对应的 vid 值: {', '.join(modified_vids_per_file[file])}")
    else:
        print("没有文件发生替换。")
    
