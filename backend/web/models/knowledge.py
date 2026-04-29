from django.db import models
from django.utils.timezone import now, localtime
from web.models.character import Character


class Knowledge(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    fileName = models.CharField(max_length=50)
    fileType = models.CharField(max_length=50)
    create_time = models.DateTimeField(default=now)
    update_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.character.author.user.username} - {self.fileName + '.' + self.fileType} - {localtime(self.create_time).strftime('%Y-%m-%d %H:%M:%S')}"