from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['GET'])
def google_login(request):
  token=request.GET.get('tokenId')
  idinfo = id_token.verify_oauth2_token(token, requests.Request(), '168406420522-apkent5peb8549sooc0hnpshra28bhoq.apps.googleusercontent.com')
  if idinfo['email_verified']:
    try:
      user = User.objects.get(email=idinfo['email'])
    except User.DoesNotExist:
      user = User()
      user.username = idinfo['name']
      # provider random default password
      user.password = make_password(BaseUserManager().make_random_password())
      user.email = idinfo['email']
      user.save()
    
    token = RefreshToken.for_user(user)  # generate token without username & password
    response = {}
    response['username'] = user.username
    response['access_token'] = str(token.access_token)
    response['refresh_token'] = str(token)
    return Response(response)

  return Response(status=200)