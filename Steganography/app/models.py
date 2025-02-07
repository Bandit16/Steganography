from django.db import models

# Create your models here.
class EncodeFile(models.Model):
    File = models.FileField(null=True , blank=True ,upload_to="customer_files/")
    Image = models.ImageField(null=True, blank=True, default='customer_images/default.png', upload_to="customer_images/")
    ModifiedImage = models.ImageField(null=True, blank=True, upload_to="modified_images/")

    def __str__(self):
        return self.File.name
class DecodeFile(models.Model):
    Image = models.ImageField(null=False, blank=False, upload_to="decode_images/")
    def __str__(self):
        return self.Image.name
    
class EncodeMessage(models.Model):
    Message = models.TextField(null=False, blank=False)
    Image = models.ImageField(null=True, blank=True, default='customer_images/default.png', upload_to="customer_images/")
    ModifiedImage = models.ImageField(null=True, blank=True, upload_to="modified_images/")
    def __str__(self):
        return self.Message

class DecodeMessage(models.Model):
    Image = models.ImageField(null=False, blank=False, upload_to="decode_images/")
    def __str__(self):
        return self.Image.name