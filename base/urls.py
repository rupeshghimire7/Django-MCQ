from django.urls import path,re_path
from . import views


# For error 404 page


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
    path('notice/delete/<int:id>',views.deleteNotice,name='deleteNotice'),
    path('notice/update/<int:id>',views.updateNotice,name='updateNotice'),
    

    #Update Delete Question  and Confirm Delete for all questions
    path('update/<int:id>',views.updateQuestion,name='update'),
    path('delete/<int:id>',views.deleteQuestion,name='delete'),
    path('confirmDelete/',views.confirmDelete,name='confirm'),
    path('deleteall/',views.deleteAll,name='deleteall'),

    #Clear all results and attempts
    path('clearattempts/',views.clearAttempts,name='clearattempts'),

    re_path(r'^.*/$', views.error404, name='error404'),


]