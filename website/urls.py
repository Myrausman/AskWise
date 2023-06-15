from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('ask_view', ask_view, name='ask_view'),
    path('mytopics_view', mytopics_view, name='mytopics_view'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('details', details, name='details'),

]