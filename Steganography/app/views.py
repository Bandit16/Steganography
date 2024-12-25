import io
from django.core.files.storage import default_storage
from PIL import Image
import numpy as np
from django.shortcuts import render
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serializers import SecretMessageSerializer
from .models import SecretMessage
from .forms import SecretMessageForm ,DecodeMessageForm
from django.http import FileResponse , HttpResponse

def string_to_binary(text):
    binary_array = np.frombuffer(text.encode(), dtype=np.uint8)
    binary_array = np.unpackbits(binary_array)
    return binary_array

def binary_to_string(binary):
    byte_array = np.packbits(binary)
    output = byte_array.tobytes().decode()
    return output

def embedd_message(arr, text):
    height, width, _ = arr.shape
    end_bits = np.array([0, 1, 1, 1, 1, 1, 1, 1], dtype=np.uint8)
    text = np.concatenate((text, end_bits))
    text_length = text.size
    i = 0
    for y in range(height):
        for x in range(width):
            if i < text_length:
                pixel_value = arr[y, x, 2]
                pixel_value = pixel_value & 0b11111110 | text[i]
                arr[y, x, 2] = pixel_value
                i += 1
    return arr

def decode_message(arr):
    height, width, _ = arr.shape

    binary = []
    count = 0
    flag = 0
    for y in range(height):
        for x in range(width):
                if flag < 7:
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
    return binary_to_string(binary)



@api_view(['POST'])
def api_home(request):
    serializer = SecretMessageSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        id = instance.id
        message = instance.Message
        file_path = instance.Image.name             
        full_path = default_storage.path(file_path)
        image = Image.open(full_path)
        arr = np.array(image)

        binary_message = string_to_binary(message)
        modified_arr = embedd_message(arr, binary_message)
        modified_image = Image.fromarray(modified_arr)

        buffer = io.BytesIO()
        modified_image.save(buffer, format='PNG')
        buffer.seek(0)
        print("working")

        # Save the modified image to the database
        product = SecretMessage.objects.get(id=id)
        product.ModifiedImage.save('modified_' + file_path, buffer, save=True)
           
        return Response({"ModifiedImage": product.ModifiedImage.path})
          
    return Response(serializer.errors, status=400)
# API test case = {"Message":"Hello World"}

def home(request):
    form = SecretMessageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            id = instance.id
            message = instance.Message
            file_path = instance.Image.name             
            full_path = default_storage.path(file_path)
            image = Image.open(full_path)
            arr = np.array(image)
            
            binary_message = string_to_binary(message)
            modified_arr = embedd_message(arr, binary_message)
            modified_image = Image.fromarray(modified_arr)
            buffer = io.BytesIO()
            modified_image.save(buffer, format='PNG')
            buffer.seek(0)

            # Save the modified image to the database
            product = SecretMessage.objects.get(id=id)
            product.ModifiedImage.save('modified_' + file_path, buffer, save=True)
            return FileResponse(open(product.ModifiedImage.path , 'rb'),as_attachment=True, filename="modified_image.png")
        print("form not valid")
    context = {
        'form': form
    }
    print("notworking")
    return render(request, 'app/home.html', context)


def decode(request):
    form = DecodeMessageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            print("form saved")
            file_path = instance.Image.name             
            full_path = default_storage.path(file_path)
            image = Image.open(full_path)
            arr = np.array(image)
            decoded_message = decode_message(arr)
            
            return HttpResponse(decoded_message)
        
    context = {
        'form': form
    }
    return render(request, 'app/decode.html', context)
       

           
            




