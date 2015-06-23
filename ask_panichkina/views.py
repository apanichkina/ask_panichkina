# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.contrib.auth import logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ask_panichkina.forms import *
from django.contrib.auth import authenticate, login

import hashlib
import os
import json
import datetime
from ask_panichkina.models import Question, Tag, Answer, Profile, Rate_answer, Rate_profile, Rate_question
# @csrf_exempt
#def helloworld(request):
#	output = '<b>Hello World!Broooo</b><br />'
#	if request.method == 'GET':
#		output += 'Get query: '
#		for x in request.GET:
#			output+= '<br/>'
#			params = request.GET.getlist(x)
#			output += '<b>' + x + '</b>' + ':'
#			for param in params:
#				output += '<br/>' + param
#	else:
#		output += 'Post query: '
#		for x in request.POST:
#			output+= '<br/>'
#			params = request.POST.getlist(x)
#			output += '<b>' + x + '</b>' + ':'
#			for param in params:
#				output += '<br/>' + param
#	html = "<html><body>%s</body></html>" % output
#	return HttpResponse(html)



#def question(request, id):
#    data = {
#        'id' : int(id),
#    }
#    return HttpResponse(json.dumps(data), content_type = 'application/json')

def index(request, order=''):

    if order == 'best':
        questions_sort = Question.objects.filter(is_deleted=0).order_by('-likes_num')
    else:
        questions_sort = Question.objects.filter(is_deleted=0).order_by('-date')
    #list = Question.objects.all()
    paginator = Paginator(questions_sort, 20)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'questions': questions, 'order': order})


def question(request, id=0):
    question_id = int(id)
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404("This question not found")
    if question.is_deleted == 1:
        raise Http404("This question is deleted")
    question.taglist = question.tags.all()
    answers_set = Answer.objects.filter(question_id=id)
    paginator = Paginator(answers_set, 30)
    page = request.GET.get('page')
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        answers = paginator.page(1)
    except EmptyPage:
        answers = paginator.page(paginator.num_pages)
    return render(request, 'question.html', {'question': question, 'answers': answers})


def getQuestionParams(questions):
    for q in questions:
        q.answers = Answer.objects.filter(question_id=q.id).count()
        q.taglist = q.tags.all()
    return questions


def sortbytag(request, tag=''):
    try:
        t = Tag.objects.get(text=tag)
        questions_sort = t.question_set.filter(is_deleted=0).order_by('-date')
    except Tag.DoesNotExist:
        questions_sort = 0
        raise Http404("Wrong tag")
    paginator = Paginator(questions_sort, 20)
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'questions': questions, 'tag': tag})


def login(request):
#    if request.user.is_authenticated():
#       return HttpResponseRedirect("/")
    errormsg = 0
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                errormsg = 'Disabled account'
        else:
            errormsg = 'Invalid login or password'
    return render(request, 'login.html', {'errormsg' : errormsg})

def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')

def ask_question(request):
    return render(request, 'ask_question.html', ())


def profile(request, name):
    userpic = 0
    if request.user.is_authenticated():
        userpic = Profile.objects.get(user=int(request.user.id)).avatar
    try:
        user = User.objects.get(username=name)
        profile = Profile.objects.get(user=user)
        user.avatar = profile.avatar_url
        user.rating = profile.rating
    except User.DoesNotExist:
        raise Http404
    return render(request, 'profile.html', {'userpic': userpic, 'profile': user})


def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            usr = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            prof = Profile.objects.create(user_id=usr.id)
            if(request.FILES):
                prof.avatar = request.FILES['avatar']
                prof.save()
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form':form, })