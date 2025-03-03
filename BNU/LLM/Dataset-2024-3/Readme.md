执行：

制作数据集：

behavior_image_classifier.py 是将标注的数据集（excel与图片）转化为json与图片分类，一步完成

但是我们中间需要进行人工检查与数据修正，一步完成失去了灵活性。

所以先将图片按照excel标注进行分类，然后检查修正图片，修正完成后再转为json

process_excel_and_copy_images.py 第一步，根据excel分类图片

generate_json.py 根据分类好的图片生成json
