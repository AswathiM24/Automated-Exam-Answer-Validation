from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login, name='student_login'),
    path('test', views.exam_test, name='student_test'),
    path('register', views.registration, name='student_register'),
    path('', views.dashboard, name='student_home'),
    path('analysis', views.analysis_answers, name='answer_analysis'),
    path('logout', views.log_out, name='student_logout'),
    path('exam', views.examination_instruction, name='dashboard_exam'),
    path('exam/portal', views.examination, name='dashboard_exam-portal'),
    path('results', views.show_results, name='dashboard_result')
]
