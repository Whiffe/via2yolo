# visual.py

visual.py 是可视化标注的框，不可视化标签

执行代码如下：
```
python visual.py --yolo_Dataset ./riseHand_Dataset --Visual_dir ./Visual
```
--yolo_Dataset是传入yolo数据集的路径，--Visual_dir传入可视化的路径

# visual2.py

visual2.py 是可视化标注的框，和可视化标签（但需要在代码中手动修改标签，labels_class）
执行代码如下：
```
python visual2.py --yolo_Dataset yolo_behavior_Dataset-2023-12-31 --Visual_dir ./Visual
```
