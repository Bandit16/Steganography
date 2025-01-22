import numpy as np
from PIL import Image
# def string_to_binary(text):
#     binary_array = [ord(char) for char in text]
#     binary_array = np.array(binary_array , dtype=np.uint8)
#     binary_array = np.unpackbits(binary_array)
#     return binary_array

# # Example usage
# text = "Hello"
# binary = string_to_binary(text)
# print(f"Binary representation of '{text}' is: {binary}")

# byte_array = np.packbits(binary)
# output = byte_array.tobytes().decode()
# print(output)
# i1 = Image.open('modified_image.png')
# print(i1.mode)
# text = np.array([0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1] , dtype=np.uint8)
# print(text[:-8])
# byte_array = np.packbits(text)
# a = byte_array.tobytes().decode()
# print(a)
# a = 'hello'
# print(a.encode())

# arr = np.frombuffer(a.encode(), dtype=np.uint8)  
# print(np.unpackbits(arr) )

file_path = 'one.png'
file_name = file_path.split('/')[-1]
print(file_name)