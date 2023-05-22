from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
import random
from itertools import chain
from django.http import HttpResponseRedirect
from django.urls import reverse


# from faker import Faker
# faker = Faker()




"""
Authentication Part
"""

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            print(user)
        except:
            print('except')
            messages.error(request, 'User does not exist!')

        user = authenticate(request, email=email, password=password)
        print("Authenticated user",user)

        if user is not None:
            login(request, user)
            print("Logged in")
            return redirect('homepage')
        
        else:
            messages.error(request, 'Username OR Password does not match!')
            print("Else")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
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
    return render(request, 'base/home.html',{'user':user})




"""
Preparing Questions
"""
@login_required(login_url='login')
def makeQuestion(request):
    if request.user.is_staff:
        form = QuestionForm()
        if request.method == 'POST':
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                qsn = request.POST.get('question')
                opt1 = request.POST.get('option1')
                opt2 = request.POST.get('option2')
                opt3 = request.POST.get('option3')
                opt4 = request.POST.get('option4')
                option = [opt1, opt2, opt3, opt4]
                question.question = qsn
                question.correct = opt1
                question.options = json.dumps(option)
                question.save()

            # print(qn_form,opt1,opt2,opt3,opt4,option,correct_form,subject)

            # q = Question.objects.create(question=qn_form, correct = correct, level=level, options = json.dumps(option))
            # q.save()
                messages.success(request, 'Question Added Successfully!')
                return redirect('prepare')
    else:
        messages.error(request, 'You cannot Access this page!')
        return  redirect('homepage')        

    return render(request, 'base/prepareQ.html', {'form': form})





"""
ALL QUESTIONS
"""
@login_required(login_url='login')
def listQuestion(request):    
    if request.user.is_staff:
        questions = Question.objects.all().order_by('-created_at')

        context = {
            'easy':questions.filter(level='E'),
            'medium':questions.filter(level='M'),
            'hard':questions.filter(level='H'),
            'easycount': Question.objects.filter(level='E').count(),
            'mediumcount': Question.objects.filter(level='M').count(),
            'hardcount': Question.objects.filter(level='H').count(),
            'condition' : len(questions) == 0
        }




        return render(request,'base/listQ.html',context) 
    else:
        messages.error(request, 'You cannot Access this page!')
        return  redirect('homepage')






# """
# Making Fake Questions
# """
# def make_100_question():
    
#     for i in range(100):
#         qn_form = faker.sentence() + "Subject2" 
#         opt1 = faker.word()
#         opt2 = faker.word()
#         opt3 = faker.word()
#         opt4 = faker.word()
#         level = random.choice(['E','M','H'])

#         correct_form = opt1
#         option = [opt1, opt2, opt3, opt4]
#         subject=Subject.objects.get(id=3)
#         print(qn_form,opt1,opt2,opt3,opt4,option,correct_form,subject,level,"/n")

#         q = Question.objects.create(question=qn_form, correct = correct_form, level=level, options = json.dumps(option),subject=subject)
#         q.save()

#     return redirect('list')


# def fakequestion(request):
#     make_100_question()
#     return redirect('list')






"""
Exam Portal : Availability Page
and
Subject Adding/Selection
"""
@login_required(login_url='login')
def checkExam(request):
    user = request.user
    if user.is_authenticated:
        subjects = Subject.objects.all()

        data = {}
        for subject in subjects:
            if Question.objects.filter(subject=subject).exists():
                easycount = Question.objects.filter(subject=subject,level='E').count()
                print(easycount)
                mediumcount = Question.objects.filter(subject=subject,level='M').count()
                print(mediumcount)
                hardcount = Question.objects.filter(subject=subject,level='H').count()
                print(hardcount)
                if easycount>=10 and mediumcount>=5 and hardcount>=5:
                    subject.availability = True
                    subject.save()
                else:
                    subject.availability = False
                    subject.save()


            return render(request,'base/checkExams.html',{'subjects':subjects,'messages':messages})

        return render(request,'base/checkExams.html',{'subjects':subjects})
    
    else:
        return redirect('studentlogin')




"""
Making Paper
"""
paper = None
def Paper():
    easy = Question.objects.filter(level='E').order_by('?')[:10]
    medium = Question.objects.filter(level='M').order_by('?')[:5]
    hard = Question.objects.filter(level='H').order_by('?')[:5]

    allQuestions = easy | medium | hard
    return allQuestions


paper=Paper()


"""
Displaying Question Paper
"""
@login_required
def examquestion(request):
    user = request.user
    if user.is_authenticated:
        if request.session.get('exam_completed'):
        # Clear the session variable
            del request.session['exam_completed']
        # Redirect the user to the homepage
            return redirect('homepage')
        print("Attempted: ",user.attempted)
        if user.attempted == False:
            allQuestions = {}
            count = 1
            easy = paper.filter(level='E').order_by('?')
            medium = paper.filter(level='M').order_by('?')
            hard = paper.filter(level='H').order_by('?')
            Qpaper = chain(easy,medium,hard)
            for question in Qpaper:
                allQuestions[question] = count
                count += 1
            user.attempted = True
            user.save()
            print("Attempted: ",user.attempted)
            
        else:
            messages.error(request, 'You have already attempted the exam!')
            return redirect('homepage')
    else:
        return redirect('studentlogin')

    return render(request,'base/exam.html',{'questions':allQuestions})







"""
Marks Calculation
"""
@login_required
def calculate_marks(request):

    if request.method == 'POST':
        questions = Question.objects.all()  
        total_marks = 0

        QnA = {}
        for question in paper:
            QnA[question] = request.POST.get('answer{}'.format(question.id))

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
                response = render(request, 'base/result.html', {})
        user = request.user
        if user.is_staff:
            user.attempted = False
            user.marks = 0
            user.save()
        else:
            user.attempted = True
            user.marks = total_marks
            user.save()
        if user.marks >= 10:
            message = "Congratulations! You have passed the exam."
        else:
            message = "Sorry! You have failed the exam. Better luck next time."



        return render(request, 'base/result.html', {'total_marks': total_marks,'questions': paper,'QnA':QnA,'message':message})
    return redirect('homepage')





"""
NoticeBoard and Notice
"""
@login_required
def noticeboard(request):
    user = request.user
    notices = NoticeBoard.objects.all()

    form = NoticeForm()
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notice')
    else:
        form = NoticeForm()
    context = {'notices':notices, 'user':user, 'form':form}
    return render(request,'base/notices.html',context)


@login_required
def notice(request,id):
    notice = NoticeBoard.objects.get(id=id)
    return render(request,'base/notice.html', {'notice':notice})





"""
Result of all students only visible to Teachers
"""
@login_required
def allResult(request):
    if request.user.is_staff:
            data = {}
            users = User.objects.filter(is_teacher=False)
            for user in users:
                if user.attempted == False:
                    remarks = 'Not Attempted'
                elif user.marks >= 13:
                    remarks = 'Pass'
                else:
                    remarks = 'Fail'
                data[user] = [remarks]

            print(data)
            print(users)
            return render(request,'base/resultList.html',{'students':data})
    
    else:
        messages.error(request, 'You cannot Access this page!')
        return  redirect('homepage')




@login_required
def deleteQuestion(request,id):
    if request.user.is_staff:
        question = Question.objects.get(id=id)
        question.delete()
        return redirect('list')

    else:
        messages.error(request, 'You cannot Access this page!')
        return  redirect('/')
    
@login_required
def updateQuestion(request,id):
    if request.user.is_staff:
        question = Question.objects.get(id=id)
        form = AllQuestionForm(instance=question)
        if request.method == 'POST':
            form = AllQuestionForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                return redirect('list')
        return render(request,'base/updateQuestion.html',{'form':form})
    else:
        messages.error(request, 'You cannot Access this page!')
        return  redirect('/')
    
@login_required
def confirmDelete(request):
    if request.user.is_staff:
        if request.user.is_staff:
            return render(request,'base/confirmDelete.html')
    else:
        messages.error(request, 'You cannot Access this page!')
        return  redirect('list')
        
@login_required
def deleteAll(request):
    if request.user.is_staff:
        Question.objects.all().delete()
        return redirect('list')
    else:
        messages.error(request, 'You cannot Access this page!')
        return  redirect('list')

@login_required
def deleteNotice(request,id):
    if request.user.is_staff:
        question = NoticeBoard.objects.get(id=id)
        question.delete()
        return redirect('notice')


@login_required
def updateNotice(request,id):
    if request.user.is_staff:
        question = NoticeBoard.objects.get(id=id)
        form = NoticeForm(instance=question)
        if request.method == 'POST':
            form = NoticeForm(request.POST, instance=question)
            if form.is_valid():
                form.save()
                return redirect('notice')
        return render(request,'base/updatenotice.html',{'form':form})
    else:
        messages.error(request, 'You cannot Access this page!')
        return  redirect('/')
   

@login_required
def clearAttempts(request):
    if request.user.is_staff:
        User.objects.all().attempted = False
        User.objects.all().marks = 0
        for user in User.objects.all():
            user.attempted = False
            user.marks = 0
            user.save()
        return redirect('results')
    else:
        messages.error(request, 'You cannot Access this page!')
        return  redirect('homepage')
    


@login_required
def error404(request):
    return render(request, 'base/404.html')