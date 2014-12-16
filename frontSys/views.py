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
def fsIndex(request,arg1,arg2):
	return render(request,"frontSys/index.html",{'acitiviyList':Activity.objects.all()})

def fsMember(request):
	return render(request,"frontSys/member.html",{'memberList':News.objects.all()})

def fsArticle(request):
	return render(request,"frontSys/article.html",{'articleList':Article.objects.all()})

def register(request):
	return render(request,"frontSys/sign_up.html")

def addUser(request):

	name = request.POST.get('name')
	email = request.POST.get('email')
	password = request.POST.get('password')
	inviting_code = request.POST.get('inviting_code')
	

	'''  check and update the state of the InvitingCode'''
	code = InvitingCode.objects.filter(code=inviting_code)

	#check the codloginCertificatee is exist 
	
	if len(code) == 0:
		return HttpResponse("The code is not exist")
	else:
		isUsed = int(code[0].isUsed)
	
	#check the code is not used
	if isUsed == 1:
		return HttpResponse("The code is not valid")
	#check the username is exist 
	checkUser = User.objects.filter(name = name)

	if ( not (len(checkUser) ==  0)):
		return HttpResponse("The username is already exist")

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
	InvitingCode.objects.filter(code=inviting_code).update(isUsed = 1)
	return HttpResponseRedirect('index.html')

def loginCertificate(request):
	

	name = request.POST.get("name")
	password = request.POST.get('password')
	encodedPassword = hashlib.md5(password).hexdigest()
	
	checkUser = User.objects.filter(name = name)
	if len(checkUser) == 0 :
		return HttpResponse("user is not exit")

	if encodedPassword != checkUser[0].password:
		return HttpResponse("password error")
	return HttpResponseRedirect("article.html")

def articleDetail(request,Oid):
	article = Article.objects.filter(id = Oid)
	if len(article) == 0:
		return HttpResponse("the article is not exist")

	return render(request,'frontSys/content.html', {'article':article[0]})