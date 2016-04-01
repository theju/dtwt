from django.db import models
from trigger.models import Trigger
from action.models import Action
from accounts.models import User


class Recipe(models.Model):
    user = models.ForeignKey(User)
    trigger = models.ForeignKey(Trigger)
    action = models.ForeignKey(Action)
    last_checked = models.DateTimeField(auto_now=True)
    trigger_params = models.TextField(default="{}")
    action_params = models.TextField(default="{}")

    def __str__(self):
        return "{0}: {1} -> {2}".format(self.user.username,
                                        self.trigger.name,
                                        self.action.name)
