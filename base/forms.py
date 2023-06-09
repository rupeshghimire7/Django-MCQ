from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User,NoticeBoard,Question,Subject
from django import forms



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']



class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio']



class NoticeForm(forms.ModelForm):
    class Meta:
        model = NoticeBoard
        fields = "__all__"




class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["subject",'level']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = "__all__"


class AllQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"