"""
WSGI config for jamboard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jamboard.settings")
#
# application = get_wsgi_application()
#
#
#








"""
WSGI config for posters project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "posters.settings")

from django.core.wsgi import get_wsgi_application


#application = get_wsgi_application()

#The below code is to pass environment variables from apache
_application = get_wsgi_application()

env_variables_to_pass = ['jamboard_client_id', 'jamboard_client_secret']


def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for var in env_variables_to_pass:
        os.environ[var] = environ.get(var, '')
    return _application(environ, start_response)

