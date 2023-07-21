from django.urls import path

from . import views
from .views import VideoView

urlpatterns =[
    path('', views.index, name='index'),
    # path("<str:v_name>/", views.v_name, name="v_room"),
    path('<int:video_id>/', VideoView.as_view(), name='video'),
]