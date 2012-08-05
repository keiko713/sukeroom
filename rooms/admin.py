from django.contrib import admin
from rooms.models import Company
from rooms.models import Question
from rooms.models import Answer


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_url', 'deleted')

admin.site.register(Company, CompanyAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_sentence', 'category', 'answer_type')

admin.site.register(Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'additional_info', 'company', 'question')

admin.site.register(Answer, AnswerAdmin)
