# models.py

from django.db import models

class ImageUpload(models.Model):
    input_image = models.ImageField(upload_to='uploads/')
    dst_image = models.ImageField(upload_to='uploads/')
    src_image = models.ImageField(upload_to='uploads/')
    output_image = models.ImageField(upload_to='output/', null=True, blank=True)
