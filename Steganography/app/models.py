from django.db import models

# Create your models here.
class SecretMessage(models.Model):
    Message = models.TextField()
    Image = models.ImageField(null=True, blank=True, default='customer_images/default.png', upload_to="customer_images/")
    ModifiedImage = models.ImageField(null=True, blank=True, upload_to="customer_images/")

    def __str__(self):
        return self.Message
class DecodeMessage(models.Model):
    Image = models.ImageField(null=False, blank=False, upload_to="decode_images/")
    Message = models.TextField()

    def __str__(self):
        return self.Message