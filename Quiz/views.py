from django.contrib.auth.models import update_last_login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from Quiz.models import *
from datetime import timedelta
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator

score = 0

#Home page
def home(request):
    return render(request,'index.html')

# #Contact Page
def contact(request):
    if request.method=="POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        message = request.POST['message']
        send_mail(
            'Message from '+fname+' '+lname,
            'From: '+email+'\n\n'+message,
            email,
            ['contact.quizworld@gmail.com'],
            fail_silently=False,
        )
        return render(request,'contact.html', {'Name':fname})
    else:
        return render(request,'contact.html')

# About Page
def about(request):
    return render(request,'about.html')

# Handling sign-up
def signup(request):
    if request.method=="POST":
        name = request.POST['Name']
        email = request.POST['email']
        password = request.POST['password']
        password_repeat = request.POST['password-repeat']
        if password == password_repeat:
            if User.objects.filter(email=email).exists():
                messages.error(request,'Email already exists')
                return redirect('/home')
            elif User.objects.filter(username=name).exists():
                messages.error(request,'Username already exists')
                return redirect('/home')
            else:
                user = User.objects.create_user(username=name, email=email, password=password)
                user.save()
                messages.success(request, 'Your account has been successfully created.')
                return redirect('/home')
        else:
            messages.error(request,'Password is not same')
            return redirect('/home')
    else:
        return HttpResponse('404 - Not Found')

#Handling login
def handlelogin(request):
    if request.method=="POST":
        email = request.POST['semail']
        password = request.POST['spassword']
        try:
            name = User.objects.get(email=email.lower()).username
        except:
            messages.warning(request,'Credentials Invalid')
            return redirect('/home')
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request,user)
            Post = Host.objects.all()
            u = User.objects.get(username=request.user)
            marks = Marks_Of_User.objects.all()
            return render(request,'user.html', {'post':Post, 'u':u, 'marks':marks})
        else:
            messages.warning(request,'Invalid Credentials. Please try again.')
            return redirect('/home')
    else:
        return HttpResponse('404 - Not Found')

# Handling logout
def handlelogout(request):
    logout(request)
    messages.success(request,'Successfully logged out.')
    return redirect('/home')

# User Page
def user(request, uid):
    if request.method == "POST":
        if all(list(map(lambda x:x in request.POST,['field','type','noq','duration', 'noc', 'dateOfRegistration', 'date']))):
            S = Host(Field=request.POST['field'], Type_of_question=request.POST['type'], No_of_questions=request.POST['noq'], Duration=timedelta(minutes=int(request.POST['duration'])), Name_of_competition=request.POST['noc'], Last_date=request.POST['dateOfRegistration'], date=request.POST['date'],
            Created_by=User.objects.get(id=uid))
            S.save()
        # host = Host.objects.all()
        # host = Host.objects.filter().order_by('-id')
        # host = Host.objects.get(id=uid)
            # Competition_name = request.POST['noc']
            # field = request.POST['field']
            type = request.POST['type']
        # Last_date=request.POST['dateOfRegistration']
            # No_of_questions = int((request.POST['noq']))
        # li = [No_of_questions]*No_of_questions
        # if type == "MCQ(Multiple Choice Questions)":
            # return render(request,'layout.html',{'Competition_name':Competition_name, 'field':field, 'type':type, 'No_of_questions':No_of_questions, 'list':li})
            if type == "MCQ(Multiple Choice Questions)":
                return render(request,'layout.html',{'host':S})
            else:
                return render(request,'layout_tita.html',{'host':S})
        # return redirect('/layout')
            # Post = Host.objects.all()
            # content = {'post':Post}
            # return render(request,'user.html', content)
            # return render(request,'user.html',data={'Competition_name':Competition_name,'field':field, 'type':type, 'No_of_questions':No_of_questions, 'Last_date':Last_date})
        else:
            u = Host.objects.get(id=uid)
            user = User.objects.get(username=u.Created_by)
            login(request,user)
            Post = Host.objects.all()
            u = User.objects.get(username=request.user)
            marks = Marks_Of_User.objects.all()
            return render(request,'user.html', {'post':Post, 'u':u, 'marks':marks})
    else:
        return HttpResponse('404 - Not Found')

#Layout for MCQ
def layout(request, uid):
    if request.method == "POST":
        s = QuestionsMCQ(host=Host.objects.get(id=uid), Question=request.POST['quest'], Option1=request.POST['op1'], Option2=request.POST['op2'], Option3=request.POST['op3'], Option4=request.POST['op4'], correct=request.POST['ans'])
        s.save()
        S = Host.objects.get(id=uid)
        return render(request,'layout.html',{'host':S})
    else:
        return HttpResponse("404 - Not Found")

#Layout for TITA
def layout_tita(request, uid):
    if request.method == "POST":
        s = QuestionsTITA(host=Host.objects.get(id=uid), Question=request.POST['quest'])
        s.save()
        S = Host.objects.get(id=uid)
        return render(request,'layout_tita.html',{'host':S})
    else:
        return HttpResponse("404 - Not Found")

#MCA Exam
def MCA(request):
    return render(request,'mcaExam.html')

# #MCA Exam
# def TITA(request):
#     return render(request,'titaExam.html')

# #MCA Exam
# def Participants(request):
#     return render(request,'par.html')

# #MCA Exam
# def Rules(request):
#     return render(request,'rules.html')

#MCA Exam
def Timer(request):
    return render(request,'timer.html')

# Handle register
def Register(request, uid):
    u = Host.objects.get(id=uid)
    user = User.objects.get(username=u.Created_by)
    login(request,user)
    Post = Host.objects.all()
    u = User.objects.get(username=request.user)
    m = Marks_Of_User(host=Host.objects.get(id=uid), user=user)
    m.save()
    marks = Marks_Of_User.objects.all()
    messages.success(request,'Successfully registered')
    return render(request,'user.html', {'post':Post, 'u':u, 'marks':marks})

def Test(request, uid):
    post = Host.objects.get(id=uid)
    if post.Type_of_question == "MCQ(Multiple Choice Questions)":
        quest = QuestionsMCQ.objects.all()
    else:
        quest = QuestionsTITA.objects.all()
    return render(request,'Timer.html',{'post':post, 'quest':quest})

#Give test (MCQ)
def GiveTest(request, uid):
    host = Host.objects.get(id=uid)
    if(host.Type_of_question == "MCQ(Multiple Choice Questions)"):
        que = QuestionsMCQ.objects.all()
        paginator = Paginator(que,1)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1
        try:
            questions = paginator.page(page)
        except:
            questions = paginator.page(paginator.num_pages)
        return render(request,'mcaExam.html', {'host':host, 'que':que, 'questions': questions})
    else:
        que = QuestionsTITA.objects.all()
        return render(request,'titaExam.html', {'host':host, 'que':que})

lst = []
def result(request, uid):
    score = sum(lst)
    u = Host.objects.get(id=uid)
    return render(request,'result.html', {'score':score, 'u':u})

# Recieving result from participants
def saveans(request):
    ans = request.GET['ans']
    ans = int(ans)
    lst.append(ans)
    pass