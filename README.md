# 0 via2yolo
via->yolo, yolo->via

via2yolo，是将via中标注的数据转化为yolo格式数据集，并且对数据集可视化与检测，检查包括数量上的检查和小点的检查。

注意：暂不支持windows，请在 macOS 或者 linux 系统上操作

环境搭建：
```
conda create --name via2yolo python=3.8 -y
```
激活环境：
```
conda activate via2yolo
```
退出环境：
```
conda deactivate
```
删除环境:
```
conda remove -n via2yolo -all
```
安装opencv
```
pip install opencv-python-headless==4.1.2.30
```


# 1 via2yolo.py
via2yolo.py是将via转化为yolo格式
```
python via2yolo.py --Via_Dataset_dir ./via_dataset --Dataset_dir ./Dataset --tain_r 0.65
```

# 2 check.py
via2yolo.py的作用就是是检查via中的框的数量和yolo格式数据集的框的数量是否一致
```
python check.py
```

# 3 visual.py
visual.py的作用可视化yolo数据集
```
python visual.py --Dataset_dir ./Dataset --Visual_dir ./Visual
```

# 4 check_dot.py
check_dot.py是将找到小点对应的图片名字（图片名字中包含路径信息）
```
python check_dot.py --dot_size 15
```
