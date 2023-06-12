from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import LevelupForm 
from .models import Levelup
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import pymongo
import sys
import json
from django.core.serializers.json import DjangoJSONEncoder
from bson import json_util
import re
from django.contrib import messages
import random
from mongo_datatables import DataTables, Editor
from .models import MongoCollection, MongoConnection

#from .utils import get_db_handle, get_collection_handle 
#from django_quiz.utils import get_db_handle, get_collection_handle

# Create your views here.

quiz_details = None

def home(request):
    return render(request, 'levelup/home.html')

def Thankyou(request):
    return render(request, 'levelup/Thankyou.html')

def signupuser(request):
    if request.method == 'GET':
       return render(request, 'levelup/signupuser.html', {'form':UserCreationForm()}) 
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('domain')
            except IntegrityError:
                return render(request, 'levelup/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'levelup/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'levelup/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'levelup/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('domain')     

@login_required
def quiz_home(request):

    global quiz_details
    global quest_no
    global message
    quizset_options = {}

    message = ""

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'        
    
    print("request.method :: " + request.method)
    print("is_ajax :: " + str(is_ajax))
 
    print("request.GET['submit_btn'] :: " + request.GET.get('submit_btn','novalue'))   
    print("request.POST['submit_btn'] :: " + request.POST.get('submit_btn','novalue'))    
  
    print("request.GET['next_btn'] :: " + request.GET.get('next_btn','novalue')) 
    print("request.POST['next_btn'] :: " + request.POST.get('next_btn','novalue'))

 
    if  request.method == 'POST' and is_ajax :      

        data = json.load(request) 
        answer_chosen = data.get('answer')
        print(answer_chosen)               

        if  answer_chosen is None :
            json_data = json.dumps({"Status":"error"})       
            print("we are here json_data :: " + json_data)    
            return HttpResponse(json_data, content_type="application/json")   

        quizset_session = json.loads(request.session['quiz_session'])  
        quizset_answer = quizset_session['Answer']   
        quizset_answer = quizset_answer.strip("\"")  
        print(quizset_answer)   

        request.session['submit_clicked'] = "yes"

        request.session['quest_no']  = request.session['quest_no'] + 1

        if 'submit_btn' in request.POST:
            print("yes submit is clicked :: ") 
        
        json_data = json.dumps( {"answer":quizset_answer, "btn_clicked":"submit_clicked"} )    
        print("we are here json_data :: " + json_data) 
 
        return HttpResponse(json_data, content_type="application/json")   

    else:

        if quiz_details is None :
            print("db already initialized")
            client = pymongo.MongoClient("localhost", 27017, maxPoolSize=50)           
            local_db = client['localdb']
            quiz_details = local_db['quiz_collection'] 
        
        submit_clicked = request.session.setdefault('submit_clicked', "no")

        if 'next_btn' in request.POST:
            radio_answer = request.POST.get('vbtn-radio','novalue')  
            
            if(radio_answer == "novalue"):
                messages.info(request, "Please select one of the options before proceeding to Next question")
                print("radio_answer :: " + radio_answer)              
            elif (submit_clicked == "no"):
                messages.info(request, "Please submit the answer before proceeding to Next Question")    
            else:
                request.session['submit_clicked'] = "no"
#               request.session['quest_no']  = request.session['quest_no'] + 1

        elif 'prev_btn' in request.POST:    
            print("Prev button clicked")
            request.session['quest_no']  = request.session['quest_no'] - 1  

        quest_no = request.session.setdefault('quest_no', 1)
 
        if  quest_no > 10 or quest_no < 1 :
            request.session['quest_no'] = 1 
            quest_no = 1
            return redirect('Thankyou')

        quizset = quiz_details.find_one({'Question_No': quest_no})
        json_string = json_util.dumps(quizset)
        request.session['quiz_session']  = json_string 

        for key, value in quizset.items():
            if key[:7] == "Option_" and key != "Option_count" and value.strip() != "" : 
                print(key, '->', value)
                quizset_options[key] = value 

        return render(request, 'levelup/quiz_home.html', {'Question_No': quizset['Question_No'], 'Question': quizset['Question'], 'Option_1': quizset['Option_1'] ,'Option_2': quizset['Option_2'], 'Option_3': quizset['Option_3'], 'Option_4': quizset['Option_4'], 'Options_cnt':4, 'quizset_options':quizset_options})

@login_required
def add_question(request):
    return render(request, 'levelup/add_question.html')

@login_required
def domain(request):
    return render(request, 'levelup/domain.html') 

@login_required
def search(request):

    quiz_tbl = {}
    quiz_tbl_new = {}
    quiz_cur = {}

    client = pymongo.MongoClient("localhost", 27017, maxPoolSize=50)           
    local_db = client['localdb']
    quiz_details = local_db['quiz_collection'] 

    quiz_cur = quiz_details.find({}, {'_id': 0}).sort([( 'Question_No', pymongo.ASCENDING)])
    
#    for key, value in quiz_tbl.items():
#        print(key, '->', value)
#        quiz_tbl[key] = value 

    ctr = 1
    quest_list = []

    for item in quiz_cur:
#       print(item)

        for key, value in item.items():
            if key == 'Question' or key == 'Question_No': 
#                print(key, '->', value)
#                key1 = key + str(ctr)
#               quiz_tbl[key1] = value
#                ctr = ctr + 1
                quest_list.append(value)

        quiz_tbl[ctr] = quest_list
        quest_list = list()
        
#       print(quiz_tbl[ctr])

        ctr = ctr + 1

#       print(quest_list)

#    print(quiz_tbl)

    for key, value in quiz_tbl.items():
#        print(key, '->', value)
        print (value[0] , '->' , value[1])



#    for each in quiz_tbl:
#        for key, value in each:
#            print(key, '->', value)
#            quizset_options[key] = value      

    return render(request, 'levelup/search.html', { 'quiz_tbl': quiz_tbl })

@login_required
def technology(request):
    return render(request, 'levelup/technology.html')

@login_required
def rewards(request):
    return render(request, 'levelup/rewards.html')

@login_required
def feedback(request):
    return render(request, 'levelup/feedback.html')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')    
