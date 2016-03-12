from django.db import models
from django.contrib.auth.models import User


round_choices = (('round0', 'Qualification Round'), ('round1', 'Round 1'), ('round2', 'Round 2'), ('round3', 'Round 3'))


class Problem(models.Model):
    title = models.CharField(max_length=128)
    round = models.CharField(max_length=10, choices=round_choices)
    url = models.URLField()

    def __str__(self):
        return self.title


class Solve(models.Model):
    problem = models.ForeignKey(Problem)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.problem.title + " - " + self.user.username

    class Meta:
        unique_together = (("problem", "user"),)

    # def save(self, *args, **kwargs):
    #     super(Solve, self).save(*args, **kwargs)
    #     sv = SolveVector.objects.filter(user=self.user)
    #     if sv.count() == 0:
    #         sv = SolveVector.objects.create(user=self.user)
    #     elif sv.count() == 1:
    #         sv = sv[0]
    #     if self.problem.round == round_choices[0][0]:
    #         sv.round0 += 1
    #     elif self.problem.round == round_choices[1][0]:
    #         sv.round1 += 1
    #     elif self.problem.round == round_choices[2][0]:
    #         sv.round2 += 1
    #     elif self.problem.round == round_choices[3][0]:
    #         sv.round3 += 1


class SolveVector(models.Model):
    user = models.OneToOneField(User)
    avatar = models.CharField(max_length=255, default='')
    round0 = models.IntegerField(default=0)
    round1 = models.IntegerField(default=0)
    round2 = models.IntegerField(default=0)
    round3 = models.IntegerField(default=0)

    def __str__(self):
        return "%s %d %d %d %d"%(self.user.username, self.round0, self.round1, self.round2, self.round3)
