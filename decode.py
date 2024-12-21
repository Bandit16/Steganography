from PIL import Image
import numpy as np

def binary_to_string(binary):
    byte_array = np.packbits(binary)
    output = byte_array.tobytes().decode()
    return output

image1 = Image.open('modified_image.png')
arr = np.array(image1)
height, width, _ = arr.shape

binary = []
count = 0
flag = 0
for y in range(height):
    for x in range(width):
            if flag < 8:
                pixel_value =  arr[y, x , 2]
                pixel_value = bin(pixel_value)
                last_bit = int(pixel_value[-1])
                if last_bit == 1:
                     flag += 1
                else:
                     flag = 0
                binary.append(last_bit)
                count +=1
binary = (np.array(binary[:-8] , dtype=np.uint8))
print('Your hidden message is :->',binary_to_string(binary))
            