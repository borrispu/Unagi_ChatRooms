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

    def getchatroomid(self):
        return self.chatroom

    def addtag(self, tag_description):

        if len(tag_description) > 0:

            # Создаем тег, если ранее такого не было

            tags = Tag.objects.filter(tag_description=tag_description)
            if len(tags) == 0:
                tag = Tag()
                tag.tag_description = tag_description
                tag.save()
            else:
                tag = tags[0]

            # Добавляем тег участнику

            self.tags.add(tag)
            self.save()

    def removetag(self, tag_description):

        if len(tag_description) > 0:

            # Ищем тег участника

            tags = Tag.objects.filter(tag_description=tag_description)
            if len(tags) > 0:
                tag = tags[0]
                self.tags.remove(tag)
                self.save()
