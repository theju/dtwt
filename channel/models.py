from django.db import models

class Channel(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __unicode__(self):
        return self.name
