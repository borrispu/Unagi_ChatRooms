from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.IntegerField()


class Tag(models.Model):
    tag_description = models.CharField(max_length=100)


class Person(models.Model):
    ticket = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    chatroom_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def get_chatroom_id(self):
        return self.chatroom_id

    def put_tag(self, tag):
        pass
