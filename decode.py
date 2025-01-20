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

binary = []
count = 0
flag = 0
for y in range(height):
    for x in range(width):
        if flag < 83:
            pixel_value = arr[y, x, 2]
            last_bit = pixel_value & 1
            binary.append(last_bit)
            if last_bit == 1:
                flag += 1
            else:
                flag = 0
            count += 1

binary = np.array(binary[:-84], dtype=np.uint8)
print(binary.size)
print('Your hidden message is :->', binary_to_zip(binary))