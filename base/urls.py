from django.urls import path
from . import views

urlpatterns = [

    #Authentication
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('homepage/', views.home, name='homepage'),

    #Homepage
    path('', views.home, name='homepage'),

    #Exam Questions
    path('prepQ', views.makeQuestion, name='prepare'),
    path('listQ',views.listQuestion, name='list'),
    # path('fakequestion',views.fakequestion,name='fakequestion'),

    #Checking Exam
    path('subjects',views.checkExam,name='checkExam'),
    path('exam',views.examquestion,name='examquestion'),

    #Results
    path('calculate-marks/', views.calculate_marks, name='calculate_marks'),
    path('results/', views.allResult, name='results'),

    #NoticeBoard
    path('notices/',views.noticeboard,name='notice'),
    path('notice/<int:id>',views.notice,name='noticeX'),





]