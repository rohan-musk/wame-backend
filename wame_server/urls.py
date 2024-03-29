from django.urls import path
from . import views

urlpatterns = [
  path('auth/googleLogin/', views.google_login, name='google_login'),
]
