from django.db import models
from django.contrib.auth.models import User


round_choices = ((0,'round0'), (1,'round1'), (2,'round2'), (3,'round3'))


class Problem(models.Model):
    title = models.CharField(max_length=128)
    round = models.CharField(max_length=10, choices=round_choices)
    user = models.ForeignKey(User)


