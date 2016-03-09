from django.http import HttpResponseRedirect
import os
import random
import string


def github_callback(request):
    return HttpResponseRedirect('admin')


def github_login(request):
    u = 'https://github.com/login/oauth/authorize?'
    u += "client_id="+os.environ['jamboard_client_id']
    u += "&redirect_uri=jamboard/callback"
    sec = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(9)])
    request.session['state'] = sec
    u += "&state="+sec
    return HttpResponseRedirect(u)


