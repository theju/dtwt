from django.db import models
from channel.models import Channel

class Action(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    channel = models.ForeignKey(Channel)
    klass = models.CharField(max_length=50)

    def __str__(self):
        return "{0} - {1}".format(self.channel.name, self.name)
