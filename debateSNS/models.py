import datetime
from django_mongodb_engine.contrib import MongoDBManager
from django.db import models
from django.utils import timezone
from djangotoolbox.fields import  ListField
from django import forms

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField()
    uploadUser = models.CharField(max_length = 100)
    objects = MongoDBManager();
    def date_format(self):
       self.date = self.date.strftime("%Y-%m-%d")
    
    def __unicode__(self):
            return self.title
        
class Product(models.Model):
    title = models.CharField(max_length=100)
    uploadUser = models.CharField(max_length = 100)
    content = models.TextField()
    
    def __unicode__(self):
            return self.title
        
class Plan(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    uploadUser = models.CharField(max_length = 100)
    
    def __unicode__(self):
            return self.title
        
class Us(models.Model):
    title = models.CharField(max_length=100)
    order = models.SmallIntegerField()
    uploadUser = models.CharField(max_length = 100)
    content = models.TextField()
    
    def __unicode__(self):
            return self.title

class User(models.Model):
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=100)

class Recruit(models.Model):
    title  = models.CharField(max_length=100)
    uploadUser = models.CharField(max_length = 100)
    content = models.TextField()

class Contact(models.Model):
    tel = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    uploadUser = models.CharField(max_length = 100)

class Image(models.Model):
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    uploadUser = models.CharField(max_length = 100)
    #file = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
    

