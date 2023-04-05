# 0 via2yolo
via->yolo, yolo->via

----

已经申请软著，相关资料链接如下：

【腾讯文档】杨帆 分享给你多个文件 [https://docs.qq.com/s/GmsJlEbZPL2QqvUMarbfxG](https://docs.qq.com/s/GmsJlEbZPL2QqvUMarbfxG)

b站视频：
[https://www.bilibili.com/video/BV1cT411e7Rr/](https://www.bilibili.com/video/BV1cT411e7Rr/)

CSDN：[https://blog.csdn.net/WhiffeYF/article/details/129750339](https://blog.csdn.net/WhiffeYF/article/details/129750339)

知乎：[https://zhuanlan.zhihu.com/p/616697149](https://zhuanlan.zhihu.com/p/616697149)

----

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
python visual.py --yolo_Dataset ./riseHand_Dataset --Visual_dir ./Visual
```

# 4 check_dot.py
check_dot.py是将找到小点对应的图片名字（图片名字中包含路径信息）
```
python check_dot.py --dot_size 15 --via_Dataset ./riseHand_via_dataset
```

# 5 yolo2via.py
yolo2via.py是将yolo的检测结果转化为via可以识别的格式
```
python yolo2via.py --img_path /root/autodl-tmp/1000 --label_path  ./runs/detect/1000/labels --json_path ./1000.json
```

# 6 png2jpg.py 
png2jpg.py 是将png格式转化为jpg格式

```
python png2jpg.py --imgIn ./riseHand_Dataset/images/ --imgOut ./VOC/JPEGImages/
```

# 7 pngCheck.py
pngCheck.py 的作用是检查via文件中图片格式是否正确
```
python pngCheck.py --riseHand_via_dataset ./riseHand_via_dataset
```

# 8 jpg2png.py
jpg2png.py 的作用是找出via文件中jpg格式的图片

由于本代码会将jpg图片转化为png格式，这就需要将原来的文件备份一次

备份的文件夹名字为：riseHand_via_dataset1
```
python jpg2png.py --riseHand_via_dataset ./riseHand_via_dataset --riseHand_via_dataset1 ./riseHand_via_dataset1
```

# 9 yolo2voc.py
yolo2voc.py的作用是将yolo格式的数据集转化为voc格式的数据集
```
python yolo2voc.py --JPEGImages ./VOC/JPEGImages/ --yoloPath ./riseHand_Dataset/labels/ --xmlPath ./VOC/Annotations/
```

# 10 countLabels.py
countLabels.py 的作用是统计yolo数据集中，每张图片标签数的范围（区间标注量统计）

如统计图片中有1～5个标签的图片数量

如统计图片中有6～10个标签的图片数量等

实现方式是计算每个txt中的行数，然后进行统计
```
python countLabels.py --dir_path riseHand_Dataset
```

```
python countLabels2.py --dir_path riseHand_Dataset
```

# 11 labels_txts_count.py
labels_txts_count.py 的作用是统计 所有txt有多少行（即对应图片中有多少标签）

并且统计有多少txt文件（即统计有多少图片）
```
python labels_txts_count.py --dir_path riseHand_Dataset
```
