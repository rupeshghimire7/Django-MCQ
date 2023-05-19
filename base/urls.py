from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),


    path('', views.home, name='homepage'),
    path('prepQ', views.makeQuestion, name='prepare'),
    path('listQ',views.listQuestion, name='list'),
    path('fakequestion',views.fakequestion,name='fakequestion'),
    path('exam',views.examquestion,name='examquestion'),
    path('calculate-marks/', views.calculate_marks, name='calculate_marks'),
    path('notices/',views.noticeboard,name='notice'),
    path('notice/<int:id>',views.notice,name='noticeX'),





]