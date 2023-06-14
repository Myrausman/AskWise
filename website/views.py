from django.shortcuts import render,redirect,get_object_or_404
import random
from database.models import *
# Create your views here.
def home(request):
    if request.method == 'POST':
            login = Login.objects.filter(email=request.POST.get('email')).first()
            return render(request, 'index.html', {'email':login.email,'login':True})
    return render(request, 'index.html', {})
def ask_view(request):
    return render(request, 'ask.html', {})
def mytopics_view(request):
    
    return render(request, 'mytopics.html')
def register(request):
    return render (request,'register.html',{})
def details(request):
    if request.method=='POST':
         questionTitle=request.POST['questionTitle']
         questionDetails=request.POST['questionDetails']
         tags=request.POST['tags']
         question=Question.objects.create(
              title=questionTitle,
              details=questionDetails,
              tag=tags
         )
         question.save()
         return redirect('/details')

    return render (request,'details.html',{})