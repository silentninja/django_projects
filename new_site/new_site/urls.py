from django.conf.urls import patterns, include, url
from django.contrib import admin
from gmail import views
urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'new_site.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', views.index),
                       url(r'^login/$', views.glogin),
                       url(r'^oauth2callback',views.oauth_callback)
                       )
