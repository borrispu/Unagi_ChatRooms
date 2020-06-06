from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField(default=0)
    occupied = models.IntegerField(default=0)

    def count(self):
        chatpersons = Person.objects.filter(chatroom=self)
        self.occupied = len(chatpersons)
        self.save()

class Tag(models.Model):
    tag_description = models.CharField(max_length=100)


class Person(models.Model):
    ticket = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.PROTECT, null=True, default=None)
    tags = models.ManyToManyField(Tag)

    def get_chatroom_id(self):
        return self.chatroom

    def put_tag(self, tag):
        pass
