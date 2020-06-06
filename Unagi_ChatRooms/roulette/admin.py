from django.contrib import admin

from .models import ChatRoom, Tag, Person

admin.site.register(ChatRoom)
admin.site.register(Tag)
admin.site.register(Person)