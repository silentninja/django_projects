from django.conf.urls import patterns, url
from list import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^list/$', views.show_anime, name='show'),
                       url(r'^add/(?P<anime_id>\d+)/$',
                           views.add_anime, name='add'),
                       url(r'^mylist/$',views.my_list,name='mylist')
                       )
