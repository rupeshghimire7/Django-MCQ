from django.contrib import admin
from .models import Question, NoticeBoard, Subject, User

# Register your models here.

admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(NoticeBoard)
