# Create your models here.
import uuid

from django.db import models
from django.urls import reverse

from accounts.models import User
from django.utils import timezone


class Stream(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, default='inactive')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_streaming = models.BooleanField(default=False)
    stream_url = models.CharField(max_length=255, blank=True, null=True)

    def start_stream(self):
        self.save()
        # Logic to start the stream, e.g., initiating the stream encoder and broadcasting
        self.status = 'active'
        if not self.is_streaming:
            self.is_streaming = True

        # Generate a unique stream URL
        stream_uuid = uuid.uuid4().hex
        self.stream_url = reverse('stream_detail', kwargs={'stream_id': self.id}) + stream_uuid

        self.start_time = timezone.now()
        self.save()

    def stop_stream(self):
        # Logic to stop the stream, e.g., stopping the stream encoder and broadcasting
        self.status = 'inactive'
        if self.is_streaming:
            self.is_streaming = False

        # Clear the stream URL
        self.stream_url = None

        self.end_time = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('stream_detail', kwargs={'stream_id': self.id})


class Content(models.Model):
    content_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    categories = models.ManyToManyField('ContentCategory', through='ContentCategoryAssociation')
    is_streaming = models.BooleanField(default=False)
    stream_url = models.URLField(blank=True, null=True)
    stream_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class ContentCategory(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['category_name']


class ContentCategoryAssociation(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    category = models.ForeignKey(ContentCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.content} --- {self.category}'
