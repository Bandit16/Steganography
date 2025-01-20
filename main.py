from PIL import Image
import numpy as np
import zipfile
import io

image1 = Image.open('test.png')

arr = np.array(image1)
print(arr.size)

height, width, _ = arr.shape
print(arr[0,0,2])

def string_to_binary(text):
    binary_array = np.frombuffer(text.encode(), dtype=np.uint8)
    binary_array = np.unpackbits(binary_array)
    return binary_array

def file_to_zip_binary(file_path):
    file_name = file_path.split('/')[-1]

    buffer = io.BytesIO()
    # zip file in the buffer
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(file_path, arcname=file_name)
    
    # Save the zip file to the directory
    # with open('file.zip', 'wb') as f:
    #     f.write(buffer.getvalue())
    
    zip_binary = np.frombuffer(buffer.getvalue(), dtype=np.uint8)
    
    # binary data to bits
    binary_array = np.unpackbits(zip_binary)
    
    return binary_array


def embedd_message(text):
    #adding 83 1's to the end of the message
    end_bits = np.array([0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] , dtype=np.uint8)
    text = np.concatenate((text, end_bits))
    text_length = text.size
    i = 0
    for y in range(height):
        for x in range(width):
            if i < text_length:
                pixel_value =  arr[y, x , 2]
                pixel_value = pixel_value & 0b11111110 |  text[i]
                arr[y,x,2] = pixel_value
                i +=1

    new_image = Image.fromarray(arr)
    new_image.save('modified_image.png')

def analyze_consecutive_bits(binary_array):
    max_consecutive_ones = 0
    max_consecutive_zeros = 0
    current_ones = 0
    current_zeros = 0
    
    for bit in binary_array:
        if bit == 1:
            current_ones += 1
            current_zeros = 0
        else:
            current_zeros += 1
            current_ones = 0
        
        if current_ones > max_consecutive_ones:
            max_consecutive_ones = current_ones
        if current_zeros > max_consecutive_zeros:
            max_consecutive_zeros = current_zeros
    
    return max_consecutive_ones, max_consecutive_zeros

def main():
    # message = input("What message do you want to hide?  ")
    # text = string_to_binary('message')
    # embedd_message(text)
    # print('your message is now hidden.')
    text = file_to_zip_binary('test.py')
    print(text)
    # a , b  = analyze_consecutive_bits(text)
    # print(a)
    # print(b)
    print(text.size)
    embedd_message(text)
    print('your file is now hidden.')

main()
