from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('stream/start/', views.start_stream, name='start_stream'),
    path('stream/stop/<int:stream_id>/', views.stop_stream, name='stop_stream'),
    path('stream/<int:stream_id>/', views.stream_detail, name='stream_detail'),
]