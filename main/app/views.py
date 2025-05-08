from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import models
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

client = MongoClient("mongodb+srv://abishekarmy:N1bogmsI16E3pyxM@prime.hwwmcie.mongodb.net/?retryWrites=true&w=majority&appName=PRIME", server_api=ServerApi('1'))
# client = MongoClient("mongodb+srv://abiraj:since13062003@cluster0.cmhton0.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
# client = MongoClient("mongodb://localhost:27017", server_api=ServerApi('1'))

db_user = client.django.user
students_data = client.django.students
# stu_data = client.django.students_data

@login_required(login_url='signin')
def data_feed(request):
    if request.method == "POST":
        excel = request.FILES["excel"]
        id = request.POST["username"]
        pwrd = request.POST["password"]
        data = pd.read_excel(excel)
        stu = {}
        roll_no=list(data['Roll No'])
        name=list(data['Name'])
        cgpa=list(data["CGPA"])
        attend_per=list(data["Attendance Percentage"])
        
        try:
            # Paths
            chrome_binary_path = r"D:\Downloads\chrome-win64\chrome-win64\chrome.exe"
            chrome_driver_path = r"D:\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

            # Chrome Options
            options = Options()
            options.binary_location = chrome_binary_path
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--remote-debugging-port=9222")  # Prevent DevTools error

            # Optional for debugging
            options.add_argument("--verbose")
            # Optional: run in visible mode (remove headless)
            # options.add_argument("--headless=new")  # Optional if you want headless mode

            # Launch browser
            service = Service(executable_path=chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            time.sleep(5)
            driver.get('http://localhost:2000')
            time.sleep(5)
            signin = driver.find_element(By.XPATH,'//*[@id="email"]')
            signin.send_keys(id)
            passw = driver.find_element(By.XPATH, '//*[@id="password"]')
            passw.send_keys(pwrd)
            getin = driver.find_element(By.XPATH, '//*[@id="signin"]/input[2]')
            getin.click()
            # driver.get('http://localhost:2000/mark_entry')
            stdns = driver.find_element(By.XPATH,'/html/body/section[2]/nav/ul/a[3]/button')
            stdns.click()

            for i in range(len(roll_no)):
                stu.update({str(roll_no[i]):[name[i], cgpa[i], attend_per[i]]})
                cgpa_field = driver.find_element(By.XPATH, '//*[@id="{}"]'.format(roll_no[i]))
                cgpa_field.send_keys(cgpa[i])
                cgpa_field = driver.find_element(By.XPATH, '//*[@id="at{}"]'.format(roll_no[i]))
                cgpa_field.send_keys(attend_per[i])
            while(True):time.sleep(10)
        except Exception as e:
            print(e)
    return render(request, 'feed_data.html')

def check_user_exist(value):
    if '@' in value: return User.objects.filter(email=value).exists()
    elif '@' not in value: return User.objects.filter(username=value).exists()

@login_required(login_url='signin')
def index(request):
    if(request.user.is_authenticated):return render(request,'index.html')
    else:return redirect('signin')

@login_required(login_url='signin')
def contacts(request):
    profiles={}
    for i in db_user.find():
        profiles.update({i['username']:i['username']})
        return render(request, 'contacts.html', {'profiles':profiles})

@login_required(login_url='signin')
def profile(request):
    if request.user.is_authenticated:
        try:
            user_data = db_user.find_one(filter={'username':request.user.username})
            # user_data = {'username':user_data['username'], 'username':user_data['username'], 'contact':user_data['contact'], 'email':user_data['email']}
            return render(request,'profile.html', {'user_data':user_data})
        except:
            messages.info(request, 'Mongo Database Error')
            return redirect('index')
    else:return redirect('signin')


@login_required(login_url='signin')
def text_recognition(request):
    try:
        if request.method == "POST":
            my_uploaded_file = request.FILES['my_uploaded_file'].read()
            db_user.insert_one(my_uploaded_file)
            print(my_uploaded_file)
            return redirect("index")
    except:messages.info(request, 'idhu vanthu... under developmentla irukey')
    return render(request, 'text_recognition.html')

@login_required(login_url='signin')
def mark_entry(request):
    if request.method == 'POST':
        data = dict(request.POST)
    return render(request,'mark_entry.html',{'students_data':students_data.find()})

@login_required(login_url='signin')
def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get("su-username")
            email=request.POST.get("su-email")
            contact = request.POST.get("contact")
            password = request.POST.get("password")
            
            client.django.user.delete_one(filter={'username':request.user.username})
            user = User.objects.get(username=request.user.username)
            user.delete()

            client.django.user.insert_one({'username':username, 'contact':contact, 'email':email, 'password':password})
            User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
        else:
            try:
                user_data = db_user.find_one(filter={'username':request.user.username})
                user_data = {'username':user_data['username'], 'contact':user_data['contact'], 'email':user_data['email']}
                return render(request,'edit-profile.html', {'user_data':user_data})
            except:
                messages.info(request, 'Mongo Database Error')
                return redirect('index')


def student_list(request):
    search=request.POST.get("search")
    students=[]
    for i in students_data.find():
        name=str(i["name"]).lower()
        roll_no=str(i["roll_no"])
        if search in name or search in roll_no:
            students.append({"roll_no":i["roll_no"],"i_no":i["i_no"],"name":i["name"]})
    
    return JsonResponse({"students_data":students})


def email(request):
    email=request.POST.get("email")
    if User.objects.filter(email=email).exists():return HttpResponse('Email-ID already exists')
    else:return HttpResponse('')
    

def username(request):
    username=request.POST.get("name").lower()
    if username=="":return HttpResponse('')
    elif username.isalnum()==False:return HttpResponse('Invalid Username')
    elif User.objects.filter(username=username).exists():return HttpResponse('Username already exists')
    else:return HttpResponse('')


def signin(request):
    try:
        if request.user.is_authenticated:
            return redirect("index")
        elif request.method == 'POST':
            email=request.POST.get("email")
            password=request.POST.get("password")
            if '@' in email:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:messages.info(request, 'invalid credentials')
            else:
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
            contact=request.POST.get("su-contact")
            email=request.POST.get("su-email")
            password=request.POST.get("su-password")
            if check_user_exist(email):messages.info(request, 'User already exist')
            else:
                client.django.user.insert_one({'username':username, 'contact':contact, 'email':email, 'password':password})
                User.objects.create_user(username=username, email=email, password=password)
                if check_user_exist(email):
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('index')
    except:messages.info(request, 'Something went wrong')
    return render(request,'signup.html')

def signout(request):
    logout(request)
    return redirect('signin')

