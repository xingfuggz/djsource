from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from bayke.permissions import IsOwnerAuthenticated

from bayke.views.rest_framework import generics


User = get_user_model()

class UpdateUserView(generics.BaykeUserRetrieveAPIView):
    pass
