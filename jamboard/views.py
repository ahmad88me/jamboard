from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from jamboard.models import *
from github import Github

import os
import random
import string
import requests


def github_callback(request):
    # users = User.objects.all()
    # return render(request, 'home.html', {'users': users})
    return HttpResponse("<h2>Hello</h2>")
    # return HttpResponseRedirect('admin')


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
    #return home(request)
    return HttpResponseRedirect('/jamboard')


def home(request):
    fake_session(request)
    return render(request, 'home.html', {'solvevectors': SolveVector.objects.all(),
                            'username': request.session['username'], 'avatar': request.session['avatar']})


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
    return HttpResponseRedirect('/')


def fake_session(request):
    if 'username' not in request.session:
        request.session['username'] = 'test user'
    if 'avatar' not in request.session:
        request.session['avatar'] = 'https://octodex.github.com/images/original.png'


def get_rounds():
    return [{'roundkey': r[0], 'roundvalue': r[1]} for r in round_choices ]