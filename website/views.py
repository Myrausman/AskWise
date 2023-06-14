from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
def home(request):
    return render(request, 'index.html', {})
def ask_view(request):
    return render(request, 'ask.html', {})
def mytopics_view(request):
    return render(request, 'mytopics.html', {})
def register(request):
    return render (request,'register.html',{})
def details(request):
    return render (request,'details.html',{})