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
from django.contrib import messages
from datetime import datetime, timedelta
import string

BASE_DIR = Path(__file__).resolve().parent.parent
userinfo = None
useremail = None

# <----------- Create your views here.--------->
from django.db.models import Count




def home(request):
    global userinfo
    with sqlite3.connect('datbase.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                topic.topic_id,
                topic.title,
                topic.details,
                topic.created_at,
                COUNT(DISTINCT replies.reply_id) AS reply_count,
                GROUP_CONCAT(DISTINCT tags.tag) AS tags,
                users.fname,
                users.lname
            FROM
                topic
                LEFT JOIN tags ON topic.topic_id = tags.topic_id
                LEFT JOIN users ON topic.email = users.email
                LEFT JOIN replies ON topic.topic_id = replies.topic_id
            GROUP BY
                topic.topic_id
            ORDER BY
                topic.topic_id
        """)
        rows = cursor.fetchall()
        
        # Prepare the data as a list of dictionaries
        column_names = [description[0] for description in cursor.description]
        topics = []
        for row in rows:
            
            topic = dict(zip(column_names, row))
            topics.append(topic)
            # Access the tags associated with the topic
            tag_string = topic['tags']
            if tag_string:
                topic['tags'] = list(set(tag_string.split(',')))  # Remove duplicate tags
            else:
                topic['tags'] = []
            # Calculate the "days ago" value
            created_at = datetime.strptime(topic['created_at'], '%Y-%m-%d %H:%M:%S')
            days_ago = (datetime.now() - created_at).days
            topic['days_ago'] = days_ago
            
    return render(request, 'index.html', {'login': userinfo is not None, 'topics': topics})



def search(request):
    global userinfo
    if request.method == 'GET':
        query = request.GET.get('search')
        query=query.lower()
    with sqlite3.connect('datbase.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT topic.topic_id,
                topic.title,
                topic.details,
                topic.created_at,
                COUNT(DISTINCT replies.reply_id) AS reply_count,
                GROUP_CONCAT(DISTINCT tags.tag) AS tags,
                users.fname,
                users.lname
            FROM
                topic
                LEFT JOIN tags ON topic.topic_id = tags.topic_id 
                LEFT JOIN users ON topic.email = users.email
                LEFT JOIN replies ON topic.topic_id = replies.topic_id
            WHERE tags.tag = ?
            GROUP BY
                topic.topic_id
            ORDER BY
                topic.topic_id
        """,(query,))
        rows = cursor.fetchall()
        
        # Prepare the data as a list of dictionaries
        column_names = [description[0] for description in cursor.description]
        topics = []
        for row in rows:
            
            topic = dict(zip(column_names, row))
            topics.append(topic)
            # Access the tags associated with the topic
            tag_string = topic['tags']
            print(topic)
            if tag_string:
                topic['tags'] = list(set(tag_string.split(',')))  # Remove duplicate tags
            else:
                topic['tags'] = []
            # Calculate the "days ago" value
            created_at = datetime.strptime(topic['created_at'], '%Y-%m-%d %H:%M:%S')
            days_ago = (datetime.now() - created_at).days
            topic['days_ago'] = days_ago
            
    return render(request, 'search.html', {'login': userinfo is not None, 'topics': topics})







def logout(request):
    global userinfo, useremail
    userinfo = None
    useremail = None
    return redirect("home")

@csrf_exempt
def ask_view(request):
    if request.method == 'POST':
        question_title = request.POST.get('questionTitle')
        question_details = request.POST.get('questionDetails')
        # tags = request.POST.get('tags').split(',')
        tags = [tag.lower() for tag in request.POST.get('tags').split(',')]

        with sqlite3.connect('datbase.db') as conn:
            cursor = conn.cursor()
            # Save the question to the topics table
            cursor.execute("INSERT INTO topic (title, details, email) VALUES (?, ?, ?)",
                           (question_title, question_details, useremail)) 
            # Retrieve the inserted topic_id
            topic_id = cursor.lastrowid
            # Save each tag along with the corresponding topic_id to the tags table
            for tag in tags:
                cursor.execute("INSERT INTO tags (topic_id, tag) VALUES (?, ?)",
                               (topic_id, tag.strip()))
            conn.commit()

        return redirect('home')  # Redirect to the homepage after submitting the question

    return render(request, 'ask.html')


def mytopics_view(request):
    global userinfo, useremail
    if userinfo:
        with sqlite3.connect('datbase.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT 
                topic.topic_id, 
                topic.title, 
                topic.details,
                COUNT(DISTINCT replies.reply_id) AS reply_count, 
                GROUP_CONCAT(DISTINCT tags.tag) AS tags
            FROM 
                topic
                JOIN users ON users.email = topic.email
                LEFT JOIN tags ON topic.topic_id = tags.topic_id
                LEFT JOIN replies ON topic.topic_id = replies.topic_id
            WHERE users.email = ?
            GROUP BY
                topic.topic_id
            
            """, (useremail,))
            rows = cursor.fetchall()
            # Prepare the data as a list of dictionaries
            column_names = [description[0] for description in cursor.description]
            topics = []
            for row in rows:
                topic = dict(zip(column_names, row))
                topics.append(topic)
                # Access the tags associated with the topic
                tag_string = topic['tags']
                if tag_string:
                    topic['tags'] = tag_string.split(',')  # Split the tag string into a list
                else:
                    topic['tags'] = []  # Set an empty list if no tags are present
            return render(request, 'mytopics.html', {'topics': topics})
    else:
        return redirect('/login')


@csrf_exempt
def login(request):
    global userinfo ,useremail
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        with sqlite3.connect('datbase.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            user_det = cursor.fetchone()
            if user_det is not None:
                db_email, db_password = user_det[2],user_det[3]
                if password == db_password:
                    userinfo=user_det
                    useremail=db_email
                    print('\n' * 20 , userinfo)
                    return redirect('/')
                else:
                    
                    return render(request, 'login.html', {'error': 'Incorrect password'})
            else:
                
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
        messages.success(request, 'You have been registered successfully! Please log in to continue.')

        return redirect('login')

    return render (request,'register.html',{})

@csrf_exempt
def details(request, topic_id):

    global useremail,userinfo
    print(userinfo)
        
    with sqlite3.connect('datbase.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM topic WHERE topic_id = ?", (topic_id,))
        topic_details = cursor.fetchone()
        # Prepare the topic details as a dictionary
        column_names = [description[0] for description in cursor.description]
        topic = dict(zip(column_names, topic_details))


        
        if request.method == 'POST':
            if userinfo is None:
                return redirect('/login') 
            else:
                answer = request.POST.get('answer')
                email=useremail
                cursor.execute("INSERT INTO replies ( topic_id,details,email,likes) VALUES ( ?, ?, ?, ?)",
                            ( topic_id,answer,email,0))
               
        # Fetch replies from the database for the current topic
        cursor.execute("SELECT * FROM replies WHERE topic_id = ?", (topic_id,))
        reply_details = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        replies = [dict(zip(column_names, reply)) for reply in reply_details]
        
            
    return render(request, 'details.html', {'topic': topic,"topic_id"   :topic_id, 'replies':replies,'useremail':useremail})
  
@csrf_exempt
def delete_data(request, reply_id):
    if request.method == "POST":
        with sqlite3.connect('datbase.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM replies WHERE reply_id = ?", (reply_id,))
            conn.commit()
    return redirect('details', topic_id=request.POST.get('topic_id'))



@csrf_exempt      
def update_data(request, reply_id):
    if request.method == "POST":
        answer = request.POST.get('answer')
        with sqlite3.connect('datbase.db') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE replies SET details = ? WHERE reply_id = ?", (answer, reply_id))
            conn.commit()
    return redirect('details', topic_id=request.POST.get('topic_id'))

@csrf_exempt
def delete_topic(request, topic_id):
    if request.method == "POST":
        with sqlite3.connect('datbase.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM topic WHERE topic_id = ?", (topic_id,))
            cursor.execute("DELETE FROM replies WHERE topic_id = ?", (topic_id,))
            cursor.execute("DELETE FROM tags WHERE topic_id = ?", (topic_id,))
            conn.commit()
    return redirect('mytopics_view')


