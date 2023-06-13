from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('ask_view', ask_view, name='ask_view'),
    path('my_topics', my_topics, name='my_topics'),


]