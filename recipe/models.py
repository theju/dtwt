from django.db import models
from trigger.models import Trigger
from action.models import Action
from accounts.models import User

class Recipe(models.Model):
    user = models.ForeignKey(User)
    trigger = models.ForeignKey(Trigger)
    action = models.ForeignKey(Action)
    last_checked = models.DateTimeField()
    trigger_json = models.TextField()
    action_json = models.TextField()

    def __unicode__(self):
        return "{0}: {1} -> {2}".format(self.user.username,
                                        self.trigger.name,
                                        self.action.name)
