from django.urls import path

from . import views


app_name = "baykeshop"

urlpatterns = [
    path('user/update/<int:pk>/', views.UpdateUserView.as_view(), name='update-user'),
]