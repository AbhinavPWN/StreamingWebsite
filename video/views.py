from django.http import FileResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from video.models import Video


# Create your views here.


def index(request):
    return render(request, "video/index.html")


class VideoView(TemplateView):
    template_name = 'video/video.html'

    def get(self, request, *args, **kwargs):
        video_id = kwargs['video_id']
        video = Video.objects.get(pk=video_id)
        response = FileResponse(open(video.file.path, 'rb'), content_type='video/mp4')
        return response

