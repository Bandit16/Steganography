from PIL import Image
import numpy as np

image1 = Image.open('disabled.png')

arr = np.array(image1)
print(arr.shape)

height, width, _ = arr.shape
print(arr[0,0,2])

def string_to_binary(text):
    binary_array = [ord(char) for char in text]
    binary_array = np.array(binary_array , dtype=np.uint8)
    binary_array = np.unpackbits(binary_array)
    return binary_array




def embedd_message(text):
    end_bits = np.array([1,1,1,1,1,1,1,1] , dtype=np.uint8)
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

def main():
    message = input("What message do you want to hide?  ")
    text = string_to_binary(message)
    embedd_message(text)
    print('your message is now hidden.')

main()


