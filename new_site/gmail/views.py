import os
import logging
import httplib2
from apiclient.discovery import build
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from gmail.models import CredentialsModel
from new_site import settings
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
from django.core.exceptions import ObjectDoesNotExist

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(
    os.path.dirname(__file__), '..', 'client_secrets.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email',
    redirect_uri='http://localhost:8000/oauth2callback')


@login_required
def index(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    http = httplib2.Http()
    http = credential.authorize(http)
    gmail_service = build("gmail", "v1", http=http)
    messages = gmail_service.users().messages().list(userId='me').execute()
    messages_body = []
    messageId = messages['messages'][0]['id']
    get_message = gmail_service.users().messages().get(
        userId='me', id=messageId).execute()
    return render_to_response('gmail/thread.html', {
        'threads': get_message,
    })


def glogin(request):
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)


def oauth_callback(request):
    if not xsrfutil.validate_token(
            settings.SECRET_KEY, request.REQUEST['state'], request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.REQUEST)
    http = httplib2.Http()
    http = credential.authorize(http)

    user_info_service = build(
        serviceName='oauth2', version='v2',
        http=http)

    user_info = user_info_service.userinfo().get().execute()
    try:
        user = User.objects.get(username=user_info['id'])
    except ObjectDoesNotExist:
        user = None

    if not user:
        user = User.objects.create_user(
            user_info['id'], user_info['email'], '')
        user.first_name = user_info['name']
        user.save()
        storage = Storage(CredentialsModel, 'id', user, 'credential')
        storage.put(credential)
        return render_to_response('gmail/thread.html', {
                                  'threads': user,
                                  })
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    if user is not None:
        login(request, user)
        return render_to_response('gmail/thread.html', {
                                  'threads': user,
                                  })

    else:
        # Return an 'invalid login' error message.
        return render_to_response('gmail/thread.html', {
                                  'threads': 'Try again later some problem',
                                  })
