from django.contrib import admin
from .models import Question, Answer

# Register your models here.
@admin.register(Question)
class ReportAdmin(admin.ModelAdmin):
	list_display = ['question', 'slug', 'created']
	list_filter = ['created']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ['post', 'content']