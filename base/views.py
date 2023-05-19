from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import random
# from faker import Faker
# faker = Faker()




"""
Authentication Part
"""

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist!')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR Password does not match!')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('homepage')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Try stronger password. Eg: A3iou#123')

    return render(request, 'base/login_register.html', {'form': form})




"""
Landing Page
"""
def home(request):
    user = request.user
    return render(request, 'exams/home.html',{'user':user})




"""
Preparing Questions
"""
def makeQuestion(request):
    if request.user.is_staff:
        if request.method == 'POST':
            qn_form = request.POST.get('question')
            opt1 = request.POST.get('option1')
            opt2 = request.POST.get('option2')
            opt3 = request.POST.get('option3')
            opt4 = request.POST.get('option4')
            level = request.POST.get('level')
            subject = request.POST.get('subject')
            correct_form = opt1
            option = [opt1, opt2, opt3, opt4]

            print(qn_form,opt1,opt2,opt3,opt4,option,correct_form,subject)

            q = Question.objects.create(question=qn_form, correct = correct_form, level=level, options = json.dumps(option))
            q.save()
            return redirect('list')
    else:
        messages.error(request, 'You cannot Access this page!')
        return  redirect('homepage')        

    return render(request, 'exams/prepareQ.html')





"""
ALL QUESTIONS
"""
def listQuestion(request):    
    if request.user.is_staff:
        questions = Question.objects.all()
        jsonDec = json.decoder.JSONDecoder()
        return render(request,'exams/listQ.html',{'questions':questions})
    else:
        messages.error(request, 'You cannot Access this page!')
        return  redirect('homepage')






# """
# Making Fake Questions
# """
# def make_100_question():
    
#     for i in range(100):
#         qn_form = faker.sentence()
#         opt1 = faker.word()
#         opt2 = faker.word()
#         opt3 = faker.word()
#         opt4 = faker.word()
#         level = random.choice(['E','M','H'])

#         correct_form = opt1
#         option = [opt1, opt2, opt3, opt4]
#         subject=Subject.objects.get(id=1)
#         print(qn_form,opt1,opt2,opt3,opt4,option,correct_form,subject,level,"/n")

#         q = Question.objects.create(question=qn_form, correct = correct_form, level=level, options = json.dumps(option),subject=subject)
#         q.save()

#     return redirect('list')


# def fakequestion(request):
#     make_100_question()
#     return redirect('list')







"""
Marks Calculation
"""
def calculate_marks(request):

    if request.method == 'POST':
        questions = Question.objects.all()  
        total_marks = 0

        for question in questions:
            level = question.level
            answer = request.POST.get('answer{}'.format(question.id))
            if level=='E':
                if answer == question.correct:
                    total_marks += 1
            elif level=='M':
                if answer == question.correct:
                    total_marks += 2
            else:
                if answer == question.correct:
                    total_marks += 3
        return render(request, 'exams/result.html', {'total_marks': total_marks})
    return render(request, 'exams/exam.html', {'questions': questions})