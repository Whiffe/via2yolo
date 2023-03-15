import os
from PIL import Image

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

imgIn="/root/autodl-tmp/riseHand_Dataset/images/train/" 
imgOut="/root/autodl-tmp/VOC/JPEGImages/"
png2jpg(imgIn,imgOut)

imgIn="/root/autodl-tmp/riseHand_Dataset/images/val/" 
png2jpg(imgIn,imgOut)


print('*' * 50)
