from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth

from jamboard.models import *
from github import Github

import os
import random
import string
import requests



def github_login(request):
    u = 'https://github.com/login/oauth/authorize?'
    u += "client_id="+os.environ['jamboard_client_id']
    #u += "&redirect_uri=http://54.88.191.135/jamboard/get_access"
    sec = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(9)])
    request.session['state'] = sec
    u += "&state="+sec
    return HttpResponseRedirect(u)


def github_get_access(request):
    client_id = os.environ['jamboard_client_id']
    client_secret = os.environ['jamboard_client_secret']
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': request.GET['code'],
        #'redirect_uri': 'http://54.88.191.135/jamboard/home'#'jamboard/get_access'#'jamboard/callback'
    }
    res = requests.post('https://github.com/login/oauth/access_token', data=data)
    atts = res.text.split('&')
    d={}
    for att in atts:
        keyv = att.split('=')
        d[keyv[0]] = keyv[1]
    print "response is: "+str(d)
    access_token = d['access_token']
    request.session['access_token'] = access_token
    g = Github(access_token)
    user = g.get_user()
    users = User.objects.filter(id=user.id)
    request.session['avatar'] = user.avatar_url
    request.session['username'] = user.login
    if len(users)==0:
        u = User.objects.create_user(username=user.login, password="test", first_name=user.name,
                                        id=user.id)
        u.save()
        sv = SolveVector.objects.create(user=u, avatar=user.avatar_url)
        sv.save()
    else:
        u = users[0]
    #return home(request)
    u.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, u)
    return HttpResponseRedirect('/jamboard')


def home(request):
    fake_session(request)
    return render(request, 'home.html', {'solvevectors': SolveVector.objects.all(), 'problems': Problem.objects.all(),
                            'username': request.session['username'], 'avatar': request.session['avatar']})


@login_required()
def add_problem(request):
    fake_session(request)
    if request.method == 'GET':
        rounds = get_rounds()
        return render(request, 'add_problem.html',
                      {'username': request.session['username'],
                        'avatar': request.session['avatar'],
                        'rounds': rounds
                       })
    else:
        title = request.POST['title']
        url = request.POST['url']
        round = request.POST['round']
        problem = Problem.objects.create(title=title, url=url, round=round)
    return HttpResponseRedirect('/jamboard')


@login_required
def add_solve(request):
    fake_session(request)
    if request.method == 'GET':
        problems = Problem.objects.all()
        return render(request, 'add_solve.html',
                      {'username': request.session['username'],
                        'avatar': request.session['avatar'],
                        'problems': problems
                       })
    else:
        problem = request.POST['problem']
        problems = Problem.objects.filter(id=problem)
        if problems.count() ==1:
            try:
                problem = problems[0]
                s = Solve.objects.create(user=request.user, problem=problem)
                s.save()
                sv = SolveVector.objects.filter(user=request.user)
                if sv.count() == 0:
                    sv = SolveVector.objects.create(user=request.user)
                elif sv.count() == 1:
                    sv = sv[0]
                if problem.round == round_choices[0][0]:
                    sv.round0 += 1
                elif problem.round == round_choices[1][0]:
                    sv.round1 += 1
                elif problem.round == round_choices[2][0]:
                    sv.round2 += 1
                elif problem.round == round_choices[3][0]:
                    sv.round3 += 1
                sv.save()
            except Exception as e:
                print "exception: <%s>"%(str(e))
    return HttpResponseRedirect('/jamboard')


def logout(request):
    fake_session(request)
    auth.logout(request)
    return HttpResponseRedirect('/jamboard')


def fake_session(request):
    if 'username' not in request.session:
        request.session['username'] = 'Login'
    if 'avatar' not in request.session:
        request.session['avatar'] = 'https://octodex.github.com/images/original.png'


def get_rounds():
    return [{'roundkey': r[0], 'roundvalue': r[1]} for r in round_choices ]