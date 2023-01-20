# via2yolo
via->yolo, yolo->via
# 1 via2yolo.py
via2yolo.py是将via转化为yolo格式
```
python via2yolo.py --tain_r 0.65
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
