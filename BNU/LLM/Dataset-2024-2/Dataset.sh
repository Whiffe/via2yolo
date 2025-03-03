#!/bin/bash

# 执行第一个 Python 文件
python Datset_Excek2LLM.py --input_dir experimental_Bridge --out_dir ./result.json

# 检查第一个 Python 文件是否执行成功
if [ $? -eq 0 ]; then
    echo "Datset_Excek2LLM.py 执行成功，开始执行 balanced_Dataset.py"
    # 执行第二个 Python 文件
    python balanced_Dataset.py --input_dir ./result.json --out_dir ./balanced_result.json
    # 检查第二个 Python 文件是否执行成功
    if [ $? -eq 0 ]; then
        echo "balanced_Dataset.py 执行成功，开始执行 imgs2oneFolder.py"
        # 执行第三个 Python 文件
        python imgs2oneFolder.py --input_dir experimental_Bridge --out_dir Bridge_Behavior
        if [ $? -eq 0 ]; then
            echo "imgs2oneFolder.py 执行成功，所有脚本执行完毕。"
        else
            echo "imgs2oneFolder.py 执行失败。"
        fi
    else
        echo "balanced_Dataset.py 执行失败。"
    fi
else
    echo "Datset_Excek2LLM.py 执行失败。"
fi
