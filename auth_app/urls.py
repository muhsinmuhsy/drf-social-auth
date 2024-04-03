from django.urls import path
from auth_app.views import *

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register')
]