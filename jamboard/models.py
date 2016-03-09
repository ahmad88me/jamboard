from django.db import models

round_choices = ('round0', 'round1', 'round2', 'round3')


class Problem(models.Model):
    title = models.CharField(max_length=128)
    round = models.CharField(max_length=10, choices=round_choices)


class JamUser(models.Model):





