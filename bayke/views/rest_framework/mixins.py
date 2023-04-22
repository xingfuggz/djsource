from django.shortcuts import render

# Create your views here.
from rest_framework import mixins
from rest_framework import generics, viewsets

from bayke.models.user import BaykeUser


class UserUpdateEmail(mixins.UpdateModelMixin):
    
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

