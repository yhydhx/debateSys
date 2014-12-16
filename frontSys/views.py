# coding: utf-8  

from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render,get_object_or_404,RequestContext
from django.views import generic
#from blog.models import Poll,Choice,Blog
from django import forms
from debateSNS.models import *
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib

# Create your views here.
def fsIndex(request):
	return render(request,"frontSys/index.html",{'acitiviyList':Activity.objects.all()})

def fsMember(request):
	return render(request,"frontSys/member.html",{'memberList':News.objects.all()})

def fsArticle(request):
	return render(request,"frontSys/article.html",{'articleList':Article.objects.all()})

def register(request):
	return render(request,"frontSys/sign_up.html")

def loginCertificate(request):
	'''IVTCode = request.POST.get('InvitingCode');
	name = request.POST.get('name')
	email = request.POST.get('email')
	password = request.POST.get('password')
	inviting_code = request.POST.get('inviting_code')
	'''
	
	name = 'dai'
	email  = 'dai@125.com'
	password = '123'
	inviting_code = '0599c195f01dc37b1abddc9fd36866ef92e51d61'


	'''  check and update the state of the InvitingCode'''
	code = InvitingCode.objects.filter(code=inviting_code)[0]
	isUsed = int(code.isUsed)
	
	if isUsed == 1:
		return HttpResponse("The code is not valid")
	else:
		InvitingCode.objects.filter(code=inviting_code).update(isUsed = 1)
	'''regitst a new user'''
	encodedPassword = hashlib.md5(password).hexdigest()
	newUser = User(
		name = name,
		email = email,
		password = encodedPassword,
		inviting_code = inviting_code,
		user_flag = 0
		)
	newUser.save()
	return HttpResponseRedirect('index.html')
