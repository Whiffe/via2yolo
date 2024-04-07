# filterImage.py
我们从上一小节[BehaviorSimilarityCalculation3.py](https://github.com/Whiffe/SCB-dataset/blob/main/Behavior-Similarity-Calculation/BehaviorSimilarityCalculation3.py)中得到了边界数据，将这些边界数据复制到filterImage.py中的变量specific_overlap_files中。

filterImage.py的作用就是将指定的文件名（图片与txt）从原始的数据集中移到另一个文件夹中。

yolo_class_extract.py的作用是从数据集中提取出我们想要的类别，生成新的数据集。如SCB数据集中有举手、看书、写字三个类别，我们想把SCB拆分为举手数据集、看书写字数据集，那么就可以用这个脚本

create_txt_labels.py，有一个文件夹里都是jpg图片，该脚本会为这个图片文件夹生成另一个与之对应的空txt文本文件夹，如images/0001.jpg，images/0002.jpg，images/0003.jpg...，就会生成labels/0001.txt，labels/0002.txt，labels/0003.txt...。这样做是为了：不含目标的图片也是很好的训练数据。一旦模型在这些数据上出 现了输出，那么肯定是误检，就会产生 loss，有助于神经网络的学习，降低误检率。
