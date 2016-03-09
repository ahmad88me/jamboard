from django.conf.urls import include, url
from django.contrib import admin
import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'jamboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'login', views.github_login),
    url(r'callback', views.github_callback),
    url(r'^admin/', include(admin.site.urls)),
]
