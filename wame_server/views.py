from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from google.oauth2 import id_token
from google.auth.transport import requests
from .serializer import CustomUserSerializer
from .models import CustomUser
import json

@api_view(['GET'])
def google_login(request):
  token=request.GET.get('tokenId')
  idinfo = id_token.verify_oauth2_token(token, requests.Request(), '168406420522-apkent5peb8549sooc0hnpshra28bhoq.apps.googleusercontent.com')
  print(request.session.__dict__)
  if idinfo['email_verified']:
    if request.session.get('user'):
      return Response(request.session['user'])
    else:
      userData = CustomUser.objects.filter(email=idinfo['email']).first()
      if userData:
        serializer = CustomUserSerializer(userData)
        serialized_data = serializer.data
      else:
        data ={
          'email': idinfo['email'],
          'name': idinfo['name'],
          'picture': idinfo['picture'],
        }
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
          userData = serializer.save()
          serialized_data = serializer.data
        else:
          return Response(serializer.errors, status=400)
      request.session['user'] = serialized_data
        
      return Response(request.session)

  return Response(status=200)