from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.forms import model_to_dict
from django.core import serializers

from Unagi_ChatRooms import settings
from roulette.models import Person, ChatRoom, Tag


def index(request):
    return render(request, 'index.html')


def status(request):
    format = request.GET.get('format', 'html')
    if format == 'json':
        return JsonResponse({
            'status': 'OK'
        })
    return HttpResponse('<h2>OK<h2>')


def contacts(request):
    return render(request, 'contacts.html')


def chatrooms(request):
    format = request.GET.get('format', 'html')
    if format == 'json':
        chatroomsdata = serializers.serialize('json', ChatRoom.objects.all())
        return JsonResponse({
            'chatrooms': chatroomsdata
        })
    return render(request, 'chatrooms.html', {
            'chatrooms': ChatRoom.objects.all()
        })


def chatroom(request, number):
    format = request.GET.get('format', 'html')
    chats = ChatRoom.objects.filter(id=number)

    if len(chats) == 1:
        chat = chats[0]
        if format == 'json':
            chatdata = serializers.serialize('json', [chat])
            return JsonResponse({
                'chatroom': chatdata
            })
        thischat = model_to_dict(chat)
        return render(request, 'chatroom.html', thischat)
    else:
        if format == 'json':
            return JsonResponse({
                'chatroom': []
            })
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
    format = request.GET.get('format', 'html')
    if format == 'json':
        personsdata = serializers.serialize('json', Person.objects.all())
        return JsonResponse({
            'persons': personsdata
        })
    return render(request, 'persons.html', {
        'persons': Person.objects.all()
    })


def person(request, number):
    format = request.GET.get('format', 'html')
    guys = Person.objects.filter(id=number)

    if len(guys) == 1:
        guy = guys[0]
        if format == 'json':
            chatdata = serializers.serialize('json', [guy])
            return JsonResponse({
                'person': chatdata
            })
        thisguy = model_to_dict(guy)
        if guy.chatroom != None:
            thisguy.update({
                'chatroom_name': guy.chatroom.name
            })
        return render(request, 'person.html', thisguy)
    else:
        if format == 'json':
            return JsonResponse({
                'person': []
            })
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
    if guy.chatroom != None:
        thisguy.update({
            'chatroom_name': guy.chatroom.name
        })

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

    thisguy = model_to_dict(guy)
    thisguy.update({
        'chatroom_name': guy.chatroom.name
    })
    return render(request, 'person.html', thisguy)


def addtagtoperson(request):
    if request.method == 'GET':
        return redirect('/roulette/persons')
    if request.method == 'POST':
        person_id = request.POST['person_id']
        tag_description = request.POST['tag_description']

    guys = Person.objects.filter(id=person_id)
    if len(guys) !=1:
        return render(request, 'persons.html', {
            'persons': Person.objects.all(),
            'error': 'Участник не определен'
        })
    guy = guys[0]
    guy.addtag(tag_description)
    thisguy = model_to_dict(guy)
    thisguy.update({
        'chatroom_name': guy.chatroom.name
    })
    return render(request, 'person.html', thisguy)


def removetagfromperson(request):
    if request.method == 'GET':
        return redirect('/roulette/persons')
    if request.method == 'POST':
        person_id = request.POST['person_id']
        tag_description = request.POST['tag_description']

    guys = Person.objects.filter(id=person_id)
    if len(guys) !=1:
        return render(request, 'persons.html', {
            'persons': Person.objects.all(),
            'error': 'Участник не определен'
        })
    guy = guys[0]
    guy.removetag(tag_description)
    thisguy = model_to_dict(guy)
    thisguy.update({
        'chatroom_name': guy.chatroom.name
    })
    return render(request, 'person.html', thisguy)


def tags(request):
    format = request.GET.get('format', 'html')
    if format == 'json':
        tagsdata = serializers.serialize('json', Tag.objects.all())
        return JsonResponse({
            'tags': tagsdata
        })
    return render(request, 'tags.html', {
        'tags': Tag.objects.all()
    })


def searchtags(request):
    if request.method == 'GET':
        return redirect('/roulette/tags')
    if request.method == 'POST':
        optionaltags = []
        thisiscsrftoken = True
        for optionaltag in request.POST:
            if thisiscsrftoken:
                thisiscsrftoken = False
            else:
                optionaltags.append(request.POST[optionaltag])

        persons = {}
        for optionaltag in optionaltags:
            tag = Tag.objects.get(tag_description=optionaltag)
            guys = Person.objects.filter(tags=tag)
            for guy in guys:
                guy_number = persons.get(guy)
                if guy_number == None:
                    persons.update({
                        guy: 1
                    })
                else:
                    persons.update({
                        guy: guy_number + 1
                    })

        return render(request, 'tags.html', {
            'tags': Tag.objects.all(),
            'persons': persons
        })
