from django.contrib import admin
from .models import EventType, TaskStatus, PracticeType, Practice, AcademicStatus, AcademicDegree, Posts, Teachers

admin.site.register(EventType)
admin.site.register(TaskStatus)
admin.site.register(PracticeType)
admin.site.register(Practice)
admin.site.register(AcademicDegree)
admin.site.register(AcademicStatus)
admin.site.register(Posts)
admin.site.register(Teachers)
