from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('ask_view', ask_view, name='ask_view'),
    path('mytopics_view', mytopics_view, name='mytopics_view'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register', register, name='register'),
    path('search/', search, name='search'),
    path('details/<int:topic_id>/', details, name='details'),
    path('delete_data/<int:reply_id>/',delete_data,name='delete_data'),
    path('update_data/<int:reply_id>/',update_data,name='update_data'),
    path('delete_topic/<int:topic_id>/',delete_topic,name='delete_topic'),

]