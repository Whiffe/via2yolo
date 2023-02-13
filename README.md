# 0 via2yolo
via->yolo, yolo->via

via2yolo，是将via中标注的数据转化为yolo格式数据集，并且对数据集可视化与检测，检查包括数量上的检查和小点的检查。


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


# 1 via2yolo1.py
via2yolo1.py是将via转化为yolo格式

注意这是 via 中只框选了举手这个动作，就是将框转化为yolo格式，行为默认为 0
```
python via2yolo1.py --riseHand_via_dataset ./riseHand_via_dataset --riseHand_Dataset ./riseHand_Dataset --tain_r 0.8
```

# 2 viaExtendAction1.py
viaExtendAction1.py是对举手的数据集进行via标注扩展，扩展更多动作
```
python viaExtendAction1.py --Dataset_dir ./Dataset --newDataset_dir ./newDataset
```

# 3 via2yolo2.py
via2yolo2.py是将via转化为yolo格式

注意这是 via 中多个动作转化为yolo格式

并且可以检查没有标注的框，并给出没有标注的图片名字
```
python via2yolo2.py --RRW_via_Dataset  ./RRW_via_Dataset --RRW_Dataset ./RRW_Dataset --tain_r 0.8
```

# 2 check.py
check.py的作用就是是检查via中的框的数量和yolo格式数据集的框的数量是否一致
```
python check.py --via_Dataset ./riseHand_via_dataset --yolo_Dataset ./riseHand_Dataset
```

# 3 visual.py
visual.py的作用可视化yolo数据集
```
python visual.py --Dataset_dir ./Dataset --Visual_dir ./Visual
```

# 4 check_dot.py
check_dot.py是将找到小点对应的图片名字（图片名字中包含路径信息）
```
python check_dot.py --dot_size 15 --via_Dataset ./riseHand_via_dataset
```
