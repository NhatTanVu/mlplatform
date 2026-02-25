from django.conf import settings
from django.db import models

# Create your models here.
class SlideUpload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=512)
    blob_name = models.CharField(max_length=1024, unique=True)
    blob_url = models.URLField(max_length=2048)
    file_size = models.BigIntegerField(null=True, blank=True)

    STATUS_CHOICES = [
        ("INIT", "INIT"),
        ("UPLOADED", "UPLOADED"),
        ("FAILED", "FAILED"),
    ]
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="INIT")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)