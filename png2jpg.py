# python png2jpg.py --imgIn ./riseHand_Dataset/images/ --imgOut ./VOC/JPEGImages/
import os
from PIL import Image
import argparse
import shutil

parser = argparse.ArgumentParser()

parser.add_argument('--imgIn', default='./riseHand_Dataset/images/',type=str)
parser.add_argument('--imgOut', default='./VOC/JPEGImages/',type=str)

arg = parser.parse_args()

imgIn = arg.imgIn
imgOut = arg.imgOut

# 清空 riseHand_Dataset 下的文件及文件夹
if os.path.exists(imgOut):
    shutil.rmtree(imgOut)

os.makedirs(imgOut)

count=0
def png2jpg(imgIn,imgOut):
    names=os.listdir(imgIn)
    
    for name in names:
        img=Image.open(imgIn+name)
        name=name.split(".")
        if name[-1] == "png":
            name[-1] = "jpg"
            name = str.join(".", name)
            try:
                r,g,b,a=img.split()
            except ValueError:
                r,g,b=img.split()
            
            img=Image.merge("RGB",(r,g,b))   
            
            to_save_path = imgOut + name
            img.save(to_save_path)
            global count
            count+=1
            print(to_save_path, "------conut：",count)
        else:
            continue

png2jpg(imgIn+'train/',imgOut)
png2jpg(imgIn+'val/',imgOut)


print('*' * 50)
