# viaExtendAction1.py
viaExtendAction1.py 是将举手一个动作扩展为三个：举手、看书、写字

# viaExtendAction2.py
viaExtendAction2.py 是将举手、看书、写字三个动作，扩展为两模块的7个动作：

【行为1：举手（raise the hand）、看书（read）、写字（write）、鼓掌（hand clap）、讨论（discuss）、趴桌（lie on the table）】单选

【行为2：说话（talk）】多选

# viaExtendAction3.py
viaExtendAction3.py 是将举手、看书、写字三个动作，扩展为三个模块的7个动作：

我们在标注过程中发现，举手与看书、写字可能同时存在，所以我们需要将举手单独放在一个模块。

【行为1：举手（raise the hand）】多选

【行为2：看书（read）、写字（write）、鼓掌（hand clap）、讨论（discuss）、趴桌（lie on the table）】单选

【行为3：说话（talk）】多选

# viaExtendAction4.py 

viaExtendAction4.py 是将举手、看书、写字三个动作(两个模块)，扩展为三个模块的7个动作

由于我们已经完成了一部分viaExtendAction2.py产生的数据，所以需要将该数据也转化为三个模块的7个动作

CSDN：[https://blog.csdn.net/WhiffeYF/article/details/135355159](https://blog.csdn.net/WhiffeYF/article/details/135355159)

# viaExtendAction5.py

viaExtendAction5.py 是将以下三个模块的动作（7个）扩展为四个模块的7+3个动作

raise the hand

read、write、hand clap、discuss、lie on the table

talk

扩展为：

raise the hand

read、write、hand clap、discuss、lie on the table

talk

bow the head、look up、turn the head

执行代码如下：

python viaExtendAction5.py  --SCB_via_org ./SCB5_jpg --SCB_via_new ./SCB5_jpg_10
