import io
from django.core.files.storage import default_storage
from PIL import Image
import numpy as np
from django.shortcuts import render
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from .serializers import *
from .models import *
from .forms import *
from django.http import FileResponse , HttpResponse
import zipfile


def string_to_binary(text):
    binary_array = np.frombuffer(text.encode(), dtype=np.uint8)
    binary_array = np.unpackbits(binary_array)
    return binary_array

def binary_to_string(binary):
    byte_array = np.packbits(binary)
    output = byte_array.tobytes().decode(errors='ignore')
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
                print("Extracted files: ", extracted_files)
                return extracted_files[0]  # Return the first extracted file's name
        return "Zip file extracted successfully"
    except zipfile.BadZipFile:
        print("Error: The provided file is not a zip file.")
        return False


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

def len_of_file(arr , pin):
    height, width, _ = arr.shape
    len_binary = []
    for y in range(height):
        for x in range(32):
                pixel_value = arr[y, x, 2]
                last_bit = pixel_value & 1
                len_binary.append(last_bit)
    # use decryption here
    len_binary = custom_decrypt(np.array(len_binary, dtype=np.uint8), pin)
    length = np.packbits(len_binary)
    length = length.view(np.uint32)[0]


    return length

def decode_file_func(arr , pin):
    height, width, _ = arr.shape
    length = len_of_file(arr , pin) + 32   
    binary = []
    count = 0
    flag = 0
    for y in range(height):
        for x in range(width):
            if count < length:
                pixel_value = arr[y, x, 2]
                last_bit = pixel_value & 1
                if count < 32:
                    pass
                else:
                    binary.append(last_bit)
                
                count += 1


    binary = np.array(binary, dtype=np.uint8)
    return binary_to_zip(binary)

def custom_encrypt(binary_data: np.ndarray, pin: str) -> np.ndarray:
    pin_bytes = string_to_binary(pin)  # Convert PIN to binary

    encrypted_bits = np.zeros_like(binary_data)
    pin_length = len(pin_bytes)

    for i in range(len(binary_data)):
        key_bit = pin_bytes[i % pin_length]  # Cycle through PIN bits
        encrypted_bits[i] = (binary_data[i] ^ key_bit) ^ ((key_bit << 1) & 1)  # New encryption formula

    return encrypted_bits

def custom_decrypt(encrypted_data: np.ndarray, pin: str) -> np.ndarray:
    pin_bytes = string_to_binary(pin)  # Convert PIN to binary

    decrypted_bits = np.zeros_like(encrypted_data)
    pin_length = len(pin_bytes)

    for i in range(len(encrypted_data)):
        key_bit = pin_bytes[i % pin_length]  # Cycle through PIN bits
        decrypted_bits[i] = (encrypted_data[i] ^ ((key_bit << 1) & 1)) ^ key_bit  # New decryption formula

    return decrypted_bits




@api_view(['POST'])
def api_encode_file(request):
    serializer = EncodeFileSerializer(data=request.data)
    if serializer.is_valid():
        pin = serializer.validated_data.pop('pin', None) # remove 'pin'
        instance = serializer.save()
        id = instance.id
        image_file_path = instance.Image.name             
        image_full_path = default_storage.path(image_file_path)

        file_path = instance.File.name
        full_path = default_storage.path(file_path)
        #convert input file to zip and convert zip to binary
        binary_zip_data = file_to_zip_binary(full_path)
        binary_zip_size = np.unpackbits(np.array([binary_zip_data.size], dtype=np.uint32).view(np.uint8))
        # encryption
        encrypted_size = custom_encrypt(binary_zip_size, pin)
        binary_message = np.concatenate((encrypted_size, binary_zip_data))

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
        product = EncodeFile.objects.get(id=id)
        product.ModifiedImage.save('modified_' + image_file_path, buffer, save=True)
        absolute_url = request.build_absolute_uri(product.ModifiedImage.url)
        print("ModifiedImage",product.ModifiedImage.path)
        print("ModifiedImage",product.ModifiedImage.url)
        return Response({"ModifiedImage": absolute_url})
          
    return Response(serializer.errors, status=400)
# API test case = {"Message":"Hello World"}

@api_view(['POST'])
def api_decode_file(request):
    serializer = DecodeFileSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        pin = serializer.validated_data.pop('pin', None) # remove 'pin'
        instance = serializer.save()
        file_path = instance.Image.name             
        full_path = default_storage.path(file_path)
        image = Image.open(full_path)
        arr = np.array(image)
        decoded_file_path = decode_file_func(arr , pin)
        # Build the absolute URL
        if decoded_file_path:
            absolute_url = request.build_absolute_uri(f'/media/extracted_files/{decoded_file_path}')

            return Response({"DecodedFile": absolute_url})  
        else:
            return Response({"DecodedFile": "Error: Incorrect Pin or The provided file doesnot contain any hidden data."})
        
    return Response(serializer.errors, status=400)

def decode_file(request):
    form = DecodeMessageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            pin = form.cleaned_data.get('pin', None)  # Extract pin from form
            instance = form.save()
            print("form saved")
            file_path = instance.Image.name             
            full_path = default_storage.path(file_path)
            image = Image.open(full_path)
            arr = np.array(image)
            decoded_file_path = decode_file_func(arr , pin)
            if decoded_file_path:
                absolute_url = default_storage.path(f'extracted_files/{decoded_file_path}')
                print("decoded file",absolute_url)
                #absolute_url = default_storage.path(f'/extracted_files/{decoded_file_path}')

                return FileResponse(open(absolute_url , 'rb'),as_attachment=True)
            else:
                return HttpResponse("Error: Incorrect Pin or The provided file doesnot contain any hidden data.")
        
    context = {
        'form': form
    }
    return render(request, 'app/for_all.html', context)
       

           
def encode_file(request):
    form = EncodeFileForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            pin = form.cleaned_data.get('pin', None)  # Extract pin from form
            instance = form.save()
            id = instance.id
            image_file_path = instance.Image.name             
            image_full_path = default_storage.path(image_file_path)

            file_path = instance.File.name
            full_path = default_storage.path(file_path)

            #convert input file to zip and convert zip to binary
            binary_zip_data = file_to_zip_binary(full_path)
            binary_zip_size = np.unpackbits(np.array([binary_zip_data.size], dtype=np.uint32).view(np.uint8))
            # encryption
            encrypted_size = custom_encrypt(binary_zip_size, pin)
            binary_message = np.concatenate((encrypted_size, binary_zip_data))

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
            product = EncodeFile.objects.get(id=id)
            product.ModifiedImage.save('modified_' + file_path, buffer, save=True)
            print("ModifiedImage",product.ModifiedImage.path)
            return FileResponse(open(product.ModifiedImage.path , 'rb'),as_attachment=True, filename="modified_image.png")
        print("form not valid")
    context = {
        'form': form
    }
    print("notworking")
    return render(request, 'app/for_all.html', context)


	
def encode_message_func(arr, text):
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

def decode_message_func(arr, pin):
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
    return binary_to_string(custom_decrypt(binary, pin))


def decode_message(request):
    form = DecodeMessageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            pin = form.cleaned_data.get('pin', None)  # Extract pin from form
            instance = form.save()
            print("form saved")
            file_path = instance.Image.name             
            full_path = default_storage.path(file_path)
            image = Image.open(full_path)
            arr = np.array(image)
            decoded_message = decode_message_func(arr, pin)
            
            return HttpResponse(decoded_message)
        
    context = {
        'form': form
    }
    return render(request, 'app/for_all.html', context)



def encode_message(request):
    form = EncodeMessageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save()
            id = instance.id
            pin = form.cleaned_data.get('pin', None)  # Extract pin from form
            print(type(pin))
            print(pin)
            message = instance.Message
            file_path = instance.Image.name             
            full_path = default_storage.path(file_path)
            image = Image.open(full_path)
            arr = np.array(image)
            
            binary_message = string_to_binary(message)
            #encryption
            encrypted_message = custom_encrypt(binary_message, pin)
            
            modified_arr = encode_message_func(arr, encrypted_message)
            modified_image = Image.fromarray(modified_arr)
            buffer = io.BytesIO()
            modified_image.save(buffer, format='PNG')
            buffer.seek(0)
            # Save the modified image to the database
            product = EncodeMessage.objects.get(id=id)
            product.ModifiedImage.save('modified_' + file_path, buffer, save=True)
            return FileResponse(open(product.ModifiedImage.path , 'rb'),as_attachment=True, filename="modified_image.png")
        print("form not valid")
    context = {
        'form': form
    }
    return render(request, 'app/for_all.html', context)


@api_view(['POST'])
def api_encode_message(request):
    serializer = EncodeMessageSerializer(data=request.data)
    if serializer.is_valid():
        pin = serializer.validated_data.pop('pin', None) # remove 'pin'
        instance = serializer.save()
        id = instance.id
        message = instance.Message
        file_path = instance.Image.name             
        full_path = default_storage.path(file_path)
        image = Image.open(full_path)
        arr = np.array(image)
        binary_message = string_to_binary(message)

        encrypted_message = custom_encrypt(binary_message, pin)
        modified_arr = encode_message_func(arr, encrypted_message)

        modified_image = Image.fromarray(modified_arr)
        buffer = io.BytesIO()
        modified_image.save(buffer, format='PNG')
        buffer.seek(0)
        print("working")
        # Save the modified image to the database
        product = EncodeMessage.objects.get(id=id)
        product.ModifiedImage.save('modified_' + file_path, buffer, save=True)
           
        absolute_url = request.build_absolute_uri(product.ModifiedImage.url)
        
        return Response({"ModifiedImage": absolute_url})          
    return Response(serializer.errors, status=400)
# API test case = {"Message":"Hello World"}

@api_view(['POST'])
def api_decode_message(request):
    serializer = DecodeMessageSerializer(data=request.data)
    if serializer.is_valid():
        pin = serializer.validated_data.pop('pin', None) # remove 'pin'
        instance = serializer.save()
        file_path = instance.Image.name             
        full_path = default_storage.path(file_path)
        image = Image.open(full_path)
        arr = np.array(image)
        decoded_message = decode_message_func(arr, pin)
        return Response({"DecodedMessage": decoded_message})  
    return Response(serializer.errors, status=400)

def about(request):
    return render(request, 'app/about.html')

def home(request):
    return render(request, 'app/home.html')

def document(request):
    return render(request, 'app/document.html')