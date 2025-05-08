from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient("mongodb+srv://abishekarmy:N1bogmsI16E3pyxM@prime.hwwmcie.mongodb.net/?retryWrites=true&w=majority&appName=PRIME", server_api=ServerApi('1'))

db_user = client.django.user
stu_data = client.django.students_data
students_data = client.classroom.students

def check_user_exist(value):
    if '@' in value: return User.objects.filter(email=value).exists()
    elif '@' not in value: return User.objects.filter(username=value).exists()

@login_required(login_url='signin')
def index(request):
    if(request.user.is_authenticated):return render(request,'index.html')
    else:return redirect('signin')
    
@login_required(login_url='signin')
def mark_entry(request):
    if request.method == 'POST':
        data = dict(request.POST)
    return render(request,'mark_entry.html',{'students_data':students_data.find()})


def signin(request):
    try:
        if request.user.is_authenticated:
            return redirect("index")
        elif request.method == 'POST':
            email=request.POST.get("email")
            password=request.POST.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:messages.info(request, 'invalid credentials')                  
    except:
        messages.info(request, 'Something went wrong')
    return render(request,'signin.html')

def signup(request):
    try:
        if request.user.is_authenticated:
            return redirect("index")
        elif request.method == 'POST':
            username=request.POST.get("su-username").lower()
            email=request.POST.get("su-email")
            password=request.POST.get("su-password")
            if check_user_exist(email):messages.info(request, 'User already exist')
            else:
                User.objects.create_user(username=username, email=email, password=password)
                if check_user_exist(email):
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('index')
    except Exception as e:messages.info(request, f'Something went wrong: {e}')
    return render(request,'signup.html')

def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def data_feed(request):
    if(request.user.is_authenticated):
        if request.method == "POST":
            excel = request.FILES["excel"]
            data = pd.read_excel(excel)
            roll_no=list(data['Roll No'])
            name=list(data['Name'])
            c = 1
            for i in range(len(roll_no)):
                # students_data.insert_one({
                #     "i_no": c,
                #     "roll_no": roll_no[i],
                #     "name": name[i],
                # })
                c += 1
    return render(request, 'feed_data.html')

def delete(request):
    print("Del")
    try:
        docs = students_data.find()
        for i in docs:
            print(i)
    except Exception as e:
        print(e)
    return redirect('index')