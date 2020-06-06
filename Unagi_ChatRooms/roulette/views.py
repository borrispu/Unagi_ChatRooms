from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import model_to_dict

from Unagi_ChatRooms import settings
from roulette.models import Person, ChatRoom, Tag


def index(request):
    return render(request, 'index.html')


def status(request):
    return HttpResponse('<h2>OK<h2>')


def contacts(request):
    return render(request, 'contacts.html')


def chatrooms(request):
    return render(request, 'chatrooms.html', {
        'chatrooms': ChatRoom.objects.all()
    })


def chatroom(request, number):
    chats = ChatRoom.objects.filter(id=number)

    if len(chats) == 1:
        chat = model_to_dict(chats[0])
        return render(request, 'chatroom.html', chat)
    else:
        return redirect('/roulette/chatrooms')


def addchatroom(request):
    if request.method == 'GET':
        return render(request, 'addchatroom.html')
    else:
        name = request.POST['name']
        capacity = request.POST['capacity']

        if len(name) == 0:
            return render(request, 'addchatroom.html', {
                'error': 'Не заполнено название'
            })
        if len(capacity) == 0:
            return render(request, 'addchatroom.html', {
                'error': 'Не заполнена вместимость'
            })

        newChatRoom = ChatRoom()
        newChatRoom.name = name
        newChatRoom.capacity = capacity
        newChatRoom.save()
        newChat = model_to_dict(newChatRoom)
        return render(request, 'chatroom.html', newChat)


def removechatroom(request, number):
    ChatRoom.objects.filter(id=number).delete()

    return redirect('/roulette/chatrooms')
