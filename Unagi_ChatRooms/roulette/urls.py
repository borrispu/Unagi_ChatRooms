from django.urls import path

from . import views

app_name = 'roulette'

urlpatterns = [
    path('', views.index, name='index'),
    path('status', views.status, name='status'),
    path('contacts', views.contacts),
    path('chatrooms', views.chatrooms),
    path('addchatroom', views.addchatroom),
    path('removechatroom/<int:number>', views.removechatroom),
    path('chatroom/<int:number>', views.chatroom)
]