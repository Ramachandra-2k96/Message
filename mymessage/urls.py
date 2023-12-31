from django.urls import path
from mymessage.views import chat_view1,custom_login1,get_m
urlpatterns = [
    path("",custom_login1,name="custom_login1"),
    path("chat_view1",chat_view1,name="chat_view1"),
    path("get_m",get_m,name="get_m"),
]
