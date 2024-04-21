import threading
from django.shortcuts import render, redirect
from .decorators import student_only
from .models import *
from django.core.exceptions import *
import hashlib
from django.db import IntegrityError
from teacher.models import Questions, Paper
from django.http import HttpResponseBadRequest, JsonResponse
from django.core import serializers
import numpy
import concurrent.futures

# import the answer_validation module from the core package
from core import answer_validation as analysis


def password_to_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    return hashlib.sha512(password_bytes).hexdigest()


def login(request):
    is_logged = request.session.get('session_identifier')
    if is_logged is not None:
        return redirect('student_home')
    if request.method == "POST":
        email = request.POST['email']
        password = password_to_hash(request.POST['password'])
        try:
            student = Login.objects.get(email=email, password=password)
            request.session['session_identifier'] = student.register_num
            return redirect('student_home')
        except ObjectDoesNotExist:
            return render(request, 'student/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'student/login.html')


def log_out(request):
    request.session.flush()
    return redirect('student_login')


def registration(request):
    if request.method == "POST":
        name = request.POST['user-name']
        email = request.POST['user-email']
        password = password_to_hash(request.POST['user-password'])
        std = request.POST['user-class']

        obj = Student()
        obj.name = name
        obj.email = email
        obj.std_class = std
        try:
            obj.save()
        except IntegrityError:
            return render(request, 'student/register.html', {'err': 'duplicate email'})

        student_obj = Student.objects.get(email=email)
        login_obj = Login()
        login_obj.register_num = student_obj.register_num
        login_obj.password = password
        login_obj.student = student_obj
        login_obj.email = email
        login_obj.save()

        return redirect('student_test')
    return render(request, 'student/register.html')


@student_only
def exam_test(request):
    std_obj = Student.objects.get(register_num=request.session['session_identifier'])
    paper = Paper.objects.get(std=std_obj.std_class, is_active=True)
    obj = Questions.objects.filter(std=std_obj.std_class, paper_code=paper)
    term = paper.paper_code
    if request.method == "POST":
        print(request.POST)
        answer: list = request.POST.getlist('answer')
        term: str = request.POST['term']
        question_number: list = request.POST.getlist('question_number')
        for ans, num in zip(answer, question_number):
            ans_obj = Answers()
            ans_obj.question_num = num
            ans_obj.answer = ans
            ans_obj.student = std_obj
            ans_obj.paper_code = term
            ans_obj.is_processing = True
            ans_obj.save()
        return redirect('student_home')
    return render(request, 'student/test.html', {'questions': obj, 'term': term, 'regNum': std_obj.register_num,
                                                 'Name': std_obj.name})


# def home(request):
#     try:
#         entry = Student.objects.get(register_num=request.session.get('session_identifier'))
#         context = {'Name': entry.name, 'logged': True}
#     except ObjectDoesNotExist:
#         pass
#         context = {'logged': False}
#     return render(request, 'student/home.html', context)


def analysis_answers(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    email = request.GET.get('email')
    password = password_to_hash(request.GET.get('password'))
    try:
        std_obj = Login.objects.get(email=email, password=password).student
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'Invalid Login Credentials'}, status=400)

    ans_obj = Answers.objects.filter(student=std_obj, is_processing=True)

    # single thread
    for i in ans_obj:
        paper = Paper.objects.get(paper_code=i.paper_code)
        ques = Questions.objects.get(question_num=i.question_num, paper_code=paper)
        similarity = analysis.similarity_analysis(analysis.models[0], [ques.answer, i.answer])
        i.mark = float("{:.2f}".format(float(numpy.round(similarity * 2, 2))))
        i.is_processing = False
        i.save()

    # multi threading ,  max_workers can be changed according to the number of threads needed
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     futures = [executor.submit(process_answer, answer) for answer in ans_obj]
    #     concurrent.futures.wait(futures)

    ret_obj = Answers.objects.filter(student=std_obj, is_processing=False).values('question_num', 'mark', 'paper_code')
    result = []
    for i in ret_obj:
        question = Questions.objects.get(question_num=i['question_num'],
                                         paper_code=Paper.objects.get(paper_code=i['paper_code']))
        result.append(
            {
                'question': question.question,
                'mark': i['mark'],
                'term': i['paper_code']
            }
        )
    print(result)
    if is_ajax:
        if request.method == 'GET':
            return JsonResponse({'context': result})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


# for multi threading
# def process_answer(answer):
#     paper = Paper.objects.get(paper_code=answer.paper_code)
#     ques = Questions.objects.get(question_num=answer.question_num, paper_code=paper)
#     similarity = analysis.similarity_analysis(analysis.models[-1], [ques.answer, answer.answer])
#     answer.mark = float("{:.2f}".format(float(numpy.round(similarity * 2, 2))))
#     answer.is_processing = False
#     answer.save()


def home(request):
    return render(request, 'student/instructions.html')


@student_only
def dashboard(request):
    std_obj = Student.objects.get(register_num=request.session['session_identifier'])
    context = {
        'active': 'Dash',
        'page': 'Home',
        'Name': std_obj.name
    }
    return render(request, 'student/dashboard/home.html', context)


@student_only
def examination_instruction(request):
    std_obj = Student.objects.get(register_num=request.session['session_identifier'])
    context = {
        'active': 'Exam',
        'page': 'Exam Instruction',
        'Name': std_obj.name
    }
    return render(request, 'student/dashboard/instruction.html', context)


@student_only
def examination(request):
    std_obj = Student.objects.get(register_num=request.session['session_identifier'])
    paper = Paper.objects.get(std=std_obj.std_class, is_active=True)
    obj = Questions.objects.filter(std=std_obj.std_class, paper_code=paper)
    term = paper.paper_code
    if request.method == "POST":
        answer: list = request.POST.getlist('answer')
        term: str = request.POST['term']
        question_number: list = request.POST.getlist('question_number')
        for ans, num in zip(answer, question_number):
            ans_obj = Answers()
            ans_obj.question_num = num
            ans_obj.answer = ans
            ans_obj.student = std_obj
            ans_obj.paper_code = term
            ans_obj.is_processing = True
            ans_obj.save()

    context = {
        'active': 'Exam',
        'page': 'Exam Portal',
        'questions': obj,
        'term': term,
        'regNum': std_obj.register_num,
        'Name': std_obj.name
    }

    return render(request, 'student/dashboard/exam.html', context)


def show_results(request):
    std_obj = Student.objects.get(register_num=request.session['session_identifier'])
    ans_obj = Answers.objects.filter(student=std_obj, is_processing=True)

    # single thread
    for i in ans_obj:
        paper = Paper.objects.get(paper_code=i.paper_code)
        ques = Questions.objects.get(question_num=i.question_num, paper_code=paper)
        similarity = analysis.similarity_analysis(analysis.models[0], [ques.answer, i.answer])
        i.mark = float("{:.2f}".format(float(numpy.round(similarity * 2, 2))))
        i.is_processing = False
        i.save()

    ret_obj = Answers.objects.filter(student=std_obj, is_processing=False).values('question_num', 'mark', 'paper_code')
    result = []
    for i in ret_obj:
        try:
            question = Questions.objects.get(question_num=i['question_num'],
                                             paper_code=Paper.objects.get(paper_code=i['paper_code']))
        except ObjectDoesNotExist:
            question = Questions()
            question.question = "Term that contain this Question deleted"
        result.append(
            {
                'question': question.question,
                'mark': i['mark'],
                'term': i['paper_code']
            }
        )

    context = {
        'active': 'Result',
        'page': 'Published Result',
        'result': result,
        'maxMark': 2,
        'Name': std_obj.name
    }
    return render(request, 'student/dashboard/result.html', context)
