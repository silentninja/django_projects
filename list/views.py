from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from list.forms import UserForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from list.models import Anime, AnimeList


def index(request):
    context = RequestContext(request)

    context_dict = {'boldmessage': "I am bold font from the context"}

    return render_to_response('list/index.html', context_dict, context)


def register(request):

    context = RequestContext(request)

    registered = False
    if request.user.is_authenticated():
        return redirect('/list')
    elif request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render_to_response('list/register.html', {'user_form': user_form, 'registered': registered}, context)


def user_login(request):

    context = RequestContext(request)
    if request.user.is_authenticated():
        return redirect('/list/')

    elif request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:

                login(request, user)
                return HttpResponseRedirect('/list/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return render_to_response('list/login.html',
                                      {'message': 'Incorrect login details'}, context)

    else:

        return render_to_response('list/login.html', {}, context)


@login_required
def add_anime(request, anime_id):
    anime = Anime(pk=anime_id)
    s, add_to_list = AnimeList.objects.get_or_create(
        user=request.user, anime_list=anime)

    return HttpResponseRedirect('/list/list/')


@login_required
def my_list(request):
    context = RequestContext(request)
    anime = AnimeList.objects.filter(user=request.user)
    return render_to_response('list/mylist.html', {'anime_list': anime}, context)


@login_required
def show_anime(request):
    context = RequestContext(request)
    anime = Anime.objects.all()
    return render_to_response('list/list.html',
                              {'anime_list': anime}, context)


@login_required
def user_logout(request):

    logout(request)

    return HttpResponseRedirect('/list/')
