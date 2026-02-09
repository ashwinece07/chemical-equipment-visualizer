from django.db import models
from django.contrib.auth.models import User
import os

class UploadedDataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='csvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=255, blank=True)
    file_size = models.IntegerField(default=0)  # in bytes
    row_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.file:
            self.filename = self.file.name
            if hasattr(self.file, 'size'):
                self.file_size = self.file.size
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.filename} by {self.user.username}"

    class Meta:
        ordering = ['-uploaded_at']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"