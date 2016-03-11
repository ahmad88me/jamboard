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
        u = User.objects.create_user(username=user.login, password="testing23904809384slkjfdaslf", first_name=user.name,
                                        id=user.id, last_name=user.avatar_url)
        u.save()
    #return home(request)
    return HttpResponseRedirect('jamboard/home')


def home(request):
    users = User.objects.all()
    return render(request, 'home.html', {'users': users, 'username': request.session['username'],
                                         'avatar': request.session['avatar']})


