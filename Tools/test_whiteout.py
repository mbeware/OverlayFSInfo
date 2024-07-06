import os
import xattr



path = "/mnt/BH-03/UpperVideo3/"

name = "Taskmaster.S06E07.WEB.h264-pong.mp4"
#name = "George Ezra - Hold My Girl.mp3"

fullname = path+name

print("test xattr module")
x = xattr.xattr(fullname)
print(x)

print("test os.getxattr")
b = os.getxattr(fullname,attribute="trusted.overlay.whiteout")

print (b)







