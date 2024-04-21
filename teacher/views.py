from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from students.views import password_to_hash
from .decorators import teacher_only
from .models import *
from students.models import *


@csrf_protect
def login(request):
    is_logged = request.session.get('tech_session')
    if is_logged is not None:
        return redirect('teacher_home')
    if request.method == "POST":
        email = request.POST['email']
        password = password_to_hash(request.POST['password'])
        try:
            teacher = Teacher.objects.get(email=email, password=password)
            request.session['tech_session'] = teacher.admin_code
            return redirect('teacher_home')
        except ObjectDoesNotExist:
            return render(request, 'teacher/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'teacher/login.html')


def log_out(request):
    request.session.flush()
    return redirect('teacher_login')


@teacher_only
def home(request):
    teacher = Teacher.objects.get(admin_code=request.session.get('tech_session'))
    context = {
        'active': 'Dash',
        'page': 'Home',
        'Name': teacher.name,
    }
    return render(request, 'teacher/dashboard/home.html', context)


@teacher_only
def exam_question_paper(request):
    teacher = Teacher.objects.get(admin_code=request.session.get('tech_session'))
    paper = Paper.objects.all()
    questions = Questions.objects.all()
    context = {
        'active': 'Exam',
        'page': 'Question Paper',
        'Name': teacher.name,
        'Questions': questions,
        'term_list': paper.values_list('paper_code', flat=True).distinct(),
        'term': paper
    }
    return render(request, 'teacher/dashboard/exam.html', context)


@teacher_only
def terms_modify(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if not is_ajax:
        return HttpResponseBadRequest('Invalid Request')
    print(request.POST)
    teacher = Teacher.objects.get(admin_code=request.session.get('tech_session'))
    paper_code = request.POST.get('paper_code')
    std = request.POST.get('std')
    active = request.POST.get('active')
    try:
        obj = Paper.objects.get(paper_code=paper_code)
    except ObjectDoesNotExist:
        obj = Paper()
    try:
        obj.paper_code = paper_code
        obj.std = std
        obj.is_active = True if active == 'true' else False
        obj.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'details': str(e)}, status=400)


@teacher_only
def delete_term(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if not is_ajax:
        return HttpResponseBadRequest('Invalid Request')
    paper_code = request.POST.get('paper_code')
    try:
        obj = Paper.objects.get(paper_code=paper_code)
        obj.delete()
        return JsonResponse({'status': 'success'})
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'failed', 'details': 'unable to delete,maybe its already deleted try to '
                                                            'refresh the page'}, status=400)


@teacher_only
def add_question(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if not is_ajax:
        return HttpResponseBadRequest('Invalid Request')
    paper_code = request.POST.get('term')
    question = request.POST.get('question')
    answer = request.POST.get('answer')
    try:
        paper = Paper.objects.get(paper_code=paper_code)
        obj = Questions()
        obj.std = paper.std
        obj.paper_code = paper
        obj.question = question
        obj.answer = answer
        obj.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'details': str(e)}, status=400)


@teacher_only
def show_results(request):
    answer = Answers.objects.all()
    teacher = Teacher.objects.get(admin_code=request.session.get('tech_session'))
    context = {
        'active': 'Dash',
        'page': 'Result',
        'Name': teacher.name,
        'result': answer,
    }
    return render(request, 'teacher/dashboard/result.html', context)