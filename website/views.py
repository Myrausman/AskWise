# <-------------------imports---------------->
from django.shortcuts import render,redirect,get_object_or_404
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import sqlite3,os,datetime,random,string
from pathlib import Path
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import sqlite3
import random
import string

BASE_DIR = Path(__file__).resolve().parent.parent

#<----------- Create your views here.--------->
def home(request):
    # if request.method == 'POST':
            # login = Login.objects.filter(email=request.POST.get('email')).first()
            # return render(request, 'index.html', {'email':login.email,'login':True})
    return render(request, 'index.html', {})




def ask_view(request):
    return render(request, 'ask.html', {})
def mytopics_view(request):
    
    return render(request, 'mytopics.html')
@csrf_exempt


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        with sqlite3.connect('datbase.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            user_det = cursor.fetchone()
            print(user_det)
            
            if user_det is not None:
                db_email, db_password = user_det[2],user_det[3]
                print('here')
                print('\n'*20)
                print(db_email, db_password) # Extract email and password from the fetched user details
                if password == db_password:
                    # Login successful, proceed with further actions
                    return render(request, 'index.html')
                else:
                    # Incorrect password
                    return render(request, 'login.html', {'error': 'Incorrect password'})
            else:
                # User not found
                return render(request, 'login.html', {'error': 'User not found'})
    
    return render(request, 'login.html')




@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Retrieve the form data
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        gender = request.POST.get('gender')


        # Insert the user data into the database
        with sqlite3.connect('datbase.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users ( fname, lname, email, password, gender) VALUES ( ?, ?, ?, ?, ?)",
                           ( first_name, last_name, email, password, gender))

        return redirect('home')

    return render (request,'register.html',{})


def details(request):
    # if request.method=='POST':
    #      questionTitle=request.POST['questionTitle']
    #      questionDetails=request.POST['questionDetails']
    #      tags=request.POST['tags']
    #      question=Question.objects.create(
    #           title=questionTitle,
    #           details=questionDetails,
    #           tag=tags
    #      )
    #      question.save()
        #  return redirect('/details')

    return render (request,'details.html',{})