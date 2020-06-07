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
    path('chatroom/<int:number>', views.chatroom),
    path('persons', views.persons),
    path('addperson', views.addperson),
    path('removeperson/<int:number>', views.removeperson),
    path('person/<int:number>', views.person),
    path('movepersontochatroom', views.movepersontochatroom),
    path('addtagtoperson', views.addtagtoperson),
    path('removetagfromperson', views.removetagfromperson),
    path('tags', views.tags),
    path('searchtags', views.searchtags)
]