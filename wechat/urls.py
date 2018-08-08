from django.urls import path
from wechat import views

urlpatterns = [
    path('', views.dash, name='chat'),
    path('send_msg/', views.send_msg, name='send_msg'),
    path('get_msg/', views.get_msg, name='get_msg'),
]
