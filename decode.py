from PIL import Image
import numpy as np
import zipfile
import io

def binary_to_zip(binary):
    byte_data = bytes(np.packbits(binary))
    zip_data = io.BytesIO(byte_data)
    try:
        with zipfile.ZipFile(zip_data, 'r') as zip_ref:
            zip_ref.extractall('extracted_files')
        return "Zip file extracted successfully"
    except zipfile.BadZipFile:
        return "File is not a zip file"

image1 = Image.open('modified_image.png')
arr = np.array(image1)
print(arr.size)
height, width, _ = arr.shape

def len_of_file():
    len_binary = []
    for y in range(height):
        for x in range(32):
                pixel_value = arr[y, x, 2]
                last_bit = pixel_value & 1
                len_binary.append(last_bit)
    defe = np.packbits(len_binary)
    defe = defe.view(np.uint32)[0]

    return defe

defe = len_of_file() + 32   
print(defe)   
binary = []
count = 0
flag = 0
for y in range(height):
    for x in range(width):
        if count < defe:
            pixel_value = arr[y, x, 2]
            last_bit = pixel_value & 1
            if count < 32:
                pass
            else:
                binary.append(last_bit)
            
            count += 1


binary = np.array(binary, dtype=np.uint8)
print(binary.size+32)
print('Your hidden message is :->', binary_to_zip(binary))