# filterImage.py
我们从上一小节[BehaviorSimilarityCalculation3.py](https://github.com/Whiffe/SCB-dataset/blob/main/Behavior-Similarity-Calculation/BehaviorSimilarityCalculation3.py)中得到了边界数据，将这些边界数据复制到filterImage.py中的变量specific_overlap_files中。

filterImage.py的作用就是将指定的文件名（图片与txt）从原始的数据集中移到另一个文件夹中。

yolo_class_extract.py的作用是从数据集中提取出我们想要的类别，生成新的数据集。如SCB数据集中有举手、看书、写字三个类别，我们想把SCB拆分为举手数据集、看书写字数据集，那么就可以用这个脚本
