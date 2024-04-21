from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="teacher_home"),
    path('login', views.login, name="teacher_login"),
    path('exam-questions', views.exam_question_paper, name='teacher_exam'),
    path('term-update', views.terms_modify, name='term_modify'),
    path('term-delete',views.delete_term,name="term_delete"),
    path('question-add',views.add_question,name="add_question"),
    path('result',views.show_results,name="show_results"),
]