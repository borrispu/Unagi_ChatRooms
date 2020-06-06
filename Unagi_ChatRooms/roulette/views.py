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


def persons(request):
    return render(request, 'persons.html', {
        'persons': Person.objects.all()
    })


def person(request, number):
    guys = Person.objects.filter(id=number)

    if len(guys) == 1:
        guy = guys[0]
        thisguy = model_to_dict(guy)
        if guy.chatroom != None:
            thisguy.update({
                'chatroom_name': guy.chatroom.name
            })
        return render(request, 'person.html', thisguy)
    else:
        return redirect('/roulette/persons')


def addperson(request):
    if request.method == 'GET':
        return render(request, 'addperson.html')
    else:
        name = request.POST['name']
        ticket = request.POST['ticket']

        if len(name) == 0:
            return render(request, 'addperson.html', {
                'error': 'Не заполнено имя'
            })
        if len(ticket) == 0:
            return render(request, 'addperson.html', {
                'error': 'Не заполнен билет'
            })

        newPerson = Person()
        newPerson.name = name
        newPerson.ticket = ticket
        newPerson.save()
        thisnewPerson = model_to_dict(newPerson)
        if newPerson.chatroom != None:
            thisnewPerson.update({
                'chatroom_name': newPerson.chatroom.name
            })
        return render(request, 'person.html', thisnewPerson)

def removeperson(request, number):
    Person.objects.filter(id=number).delete()

    return redirect('/roulette/persons')


def movepersontochatroom(request):
    if request.method == 'GET':
        return redirect('/roulette/persons')
    if request.method == 'POST':
        person_id = request.POST['person_id']
        chatroom_id = request.POST['chatroom_id']

    # Проверяем участника

    guys = Person.objects.filter(id=person_id)
    if len(guys) !=1:
        return render(request, 'persons.html', {
            'persons': Person.objects.all(),
            'error': 'Участник не определен'
        })
    guy = guys[0]
    thisguy = model_to_dict(guy)

    # Проверяем комнату

    chats = ChatRoom.objects.filter(id=chatroom_id)
    if len(chats) !=1:
        thisguy.update({
            'error': 'Комната не определена'
        })
        return render(request, 'person.html', thisguy)
    chat = chats[0]

    # Проверяем вместимость комнаты

    if chat.occupied + 1 > chat.capacity:
        thisguy.update({
            'error': 'Комната переполнена'
        })
        return render(request, 'person.html', thisguy)

    # Помещаем участника в новую комнату, пересчитываем количество в старой и новой комнатах

    currentchatroom = guy.chatroom

    guy.chatroom = chat
    guy.save()

    if currentchatroom != None:
        currentchatroom.count()
    chat.count()
    
    thisguy.update({
        'chatroom_name': guy.chatroom.name
    })
    return render(request, 'person.html', thisguy)