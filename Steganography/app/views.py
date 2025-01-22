import io
from django.core.files.storage import default_storage
from PIL import Image
import numpy as np
from django.shortcuts import render
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serializers import SecretMessageSerializer , DecodeMessageSerializer
from .models import SecretMessage
from .forms import SecretMessageForm ,DecodeMessageForm
from django.http import FileResponse , HttpResponse
import zipfile


def string_to_binary(text):
    binary_array = np.frombuffer(text.encode(), dtype=np.uint8)
    binary_array = np.unpackbits(binary_array)
    return binary_array

def binary_to_string(binary):
    byte_array = np.packbits(binary)
    output = byte_array.tobytes().decode()
    return output

def file_to_zip_binary(file_path):
    file_name = file_path.split('/')[-1]

    buffer = io.BytesIO()
    # zip file in the buffer
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(file_path, arcname=file_name)
    

    zip_binary = np.frombuffer(buffer.getvalue(), dtype=np.uint8)
    
    # binary data to bits
    binary_array = np.unpackbits(zip_binary)
    
    return binary_array

def binary_to_zip(binary):
    byte_data = bytes(np.packbits(binary))
    zip_data = io.BytesIO(byte_data)
    try:
        with zipfile.ZipFile(zip_data, 'r') as zip_ref:
            zip_ref.extractall('media/extracted_files')
            extracted_files = zip_ref.namelist()
            if extracted_files:
                return extracted_files[0]  # Return the first extracted file's name
        return "Zip file extracted successfully"
    except zipfile.BadZipFile:
        return "File is not a zip file"


def embedd_file(arr, text):
    height, width, _ = arr.shape
    text_length = text.size
    i = 0
    for y in range(height):
        for x in range(width):
            if i < text_length:
                pixel_value =  arr[y, x , 2]
                pixel_value = pixel_value & 0b11111110 |  text[i]
                arr[y,x,2] = pixel_value
                i +=1

    return arr

def len_of_file(arr):
    height, width, _ = arr.shape
    len_binary = []
    for y in range(height):
        for x in range(32):
                pixel_value = arr[y, x, 2]
                last_bit = pixel_value & 1
                len_binary.append(last_bit)
    defe = np.packbits(len_binary)
    defe = defe.view(np.uint32)[0]

    return defe

def decode_file(arr):
    height, width, _ = arr.shape
    defe = len_of_file(arr) + 32   
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
    return binary_to_zip(binary)




@api_view(['POST'])
def api_home(request):
    serializer = SecretMessageSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        id = instance.id
        message = instance.Message
        image_file_path = instance.Image.name             
        image_full_path = default_storage.path(image_file_path)

        file_path = instance.File.name
        full_path = default_storage.path(file_path)
        #convert input file to zip and convert zip to binary
        text = file_to_zip_binary(full_path)
        text_size_binary = np.unpackbits(np.array([text.size], dtype=np.uint32).view(np.uint8))
        binary_message = np.concatenate((text_size_binary,text))


        image = Image.open(image_full_path)
        arr = np.array(image)
        #for message
        # binary_message = string_to_binary(message)
        #for file
        modified_arr = embedd_file(arr, binary_message)
        modified_image = Image.fromarray(modified_arr)
        buffer = io.BytesIO()
        modified_image.save(buffer, format='PNG')
        buffer.seek(0)

        # Save the modified image to the database
        product = SecretMessage.objects.get(id=id)
        product.ModifiedImage.save('modified_' + image_file_path, buffer, save=True)
        absolute_url = request.build_absolute_uri(product.ModifiedImage.url)
        print("ModifiedImage",product.ModifiedImage.path)
        print("ModifiedImage",product.ModifiedImage.url)
        return Response({"ModifiedImage": absolute_url})
          
    return Response(serializer.errors, status=400)
# API test case = {"Message":"Hello World"}

@api_view(['POST'])
def api_decode(request):
    serializer = DecodeMessageSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        instance = serializer.save()
        file_path = instance.Image.name             
        full_path = default_storage.path(file_path)
        image = Image.open(full_path)
        arr = np.array(image)
        decoded_file_path = decode_file(arr)
        # Build the absolute URL
        absolute_url = request.build_absolute_uri(f'/media/extracted_files/{decoded_file_path}')

        return Response({"DecodedFile": absolute_url})
        
    return Response(serializer.errors, status=400)

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
            decoded_file_path = decode_file(arr)
            absolute_url = default_storage.path(f'extracted_files/{decoded_file_path}')
            print("decoded file",absolute_url)
            #absolute_url = default_storage.path(f'/extracted_files/{decoded_file_path}')

            return FileResponse(open(absolute_url , 'rb'),as_attachment=True)
        
    context = {
        'form': form
    }
    return render(request, 'app/decode.html', context)
       

           
def home(request):
    form = SecretMessageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            id = instance.id
            message = instance.Message
            image_file_path = instance.Image.name             
            image_full_path = default_storage.path(image_file_path)

            file_path = instance.File.name
            full_path = default_storage.path(file_path)
            #convert input file to zip and convert zip to binary
            text = file_to_zip_binary(full_path)
            text_size_binary = np.unpackbits(np.array([text.size], dtype=np.uint32).view(np.uint8))
            binary_message = np.concatenate((text_size_binary,text))


            image = Image.open(image_full_path)
            arr = np.array(image)
            #for message
            # binary_message = string_to_binary(message)
            #for file
            modified_arr = embedd_file(arr, binary_message)
            modified_image = Image.fromarray(modified_arr)
            buffer = io.BytesIO()
            modified_image.save(buffer, format='PNG')
            buffer.seek(0)

            # Save the modified image to the database
            product = SecretMessage.objects.get(id=id)
            product.ModifiedImage.save('modified_' + file_path, buffer, save=True)
            print("ModifiedImage",product.ModifiedImage.path)
            return FileResponse(open(product.ModifiedImage.path , 'rb'),as_attachment=True, filename="modified_image.png")
        print("form not valid")
    context = {
        'form': form
    }
    print("notworking")
    return render(request, 'app/home.html', context)




