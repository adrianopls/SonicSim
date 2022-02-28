# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 10:50:46 2022

@author: Adriano
"""

from PIL import Image
import numpy as np

w, h = 512, 300

print(type(w))
print(type(h))




#data = np.zeros((h, w, 3), dtype=np.uint8)

data = np.ones((h, w), dtype=np.ubyte) #dtype=np.uint8)
data *= 255


print(data)


#img = Image.fromarray(data, mode="L")
img = Image.open(r'C:\Users\Adriano\Desktop\vale_sub.png')

data = np.asarray(img)
print(data)
print(data.shape)

# img = Image.new("1", (h, w))
# pixels = img.load()

# for i in range(h):
#     for j in range(w):
#         pixels[i, j] = data[i][j]



#data[0:256, 0:256] = [255, 0, 0] # red patch in upper left
#img = Image.fromarray(data, 'RGB')



img.save('my_008.png')
img.show()