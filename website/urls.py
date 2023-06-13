from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('ask_view', ask_view, name='ask_view'),
    path('mytopics_view', mytopics_view, name='mytopics_view'),

]