from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=200, unique=True, null=True)
    bio = models.TextField(null=True,blank=True)
    marks = models.IntegerField(default=0)
    is_teacher = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



class Subject(models.Model):
    subject = models.CharField(max_length=50,null=True,blank=False)
    SubCode = models.CharField(max_length=10,null=True)
    year = models.CharField(max_length=3,null=True,blank=False,default='1st')

    def __str__(self):
        return self.subject


# class College(models.Model):
#     institute = models.CharField(max_length=200,null=True,blank=False)
#     code = models.CharField(max_length=5,null=True,blank=False)

#     def __str__(self):
#         return f"{self.code} ----->>  {self.institute} "



class NoticeBoard(models.Model):
    title = models.CharField(max_length=50,default="Title")
    notice = models.CharField(max_length = 1500,blank=True, default=" ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

level = {
    ('E','Easy'),
    ('M','Medium'),
    ('H','Hard')
}

class Question(models.Model):
    question = models.CharField(max_length=500,default="x",blank=False)
    correct = models.CharField(max_length=200,default="x", blank=False)
    options = models.TextField(default='options')
    level = models.CharField(max_length=1, default='E', blank=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.question[:50]


    def get_question(self):
        return self.question


# class Student(models.Model):
#     name = models.CharField(max_length=100, blank=False, null=False)
#     age = models.IntegerField(default=16)
#     roll = models.CharField(default='PAS076BCT025',max_length=12)
#     avatar = models.ImageField(null=True, default='avatar.svg')
#     bio = models.TextField(null=True)


#     def __str__(self):
#         return self.name
