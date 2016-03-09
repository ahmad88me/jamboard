from django.http import HttpResponseRedirect


def github_callback(request):
    return HttpResponseRedirect('/admin')


def github_login(request):
    u = 'https://github.com/login/oauth/authorize'
    return HttpResponseRedirect(u)

