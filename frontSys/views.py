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
def Index(request):
	return render(request,"frontSys/index.html")

def Member(request):
	return render(request,"frontSys/member.html")

def Article(request):
	return render(request,"frontSys/article.html")

def Register(request):
	return render(request,"frontSys/sign_up.html")

