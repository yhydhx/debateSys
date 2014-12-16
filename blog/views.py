# coding: utf-8  
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render,get_object_or_404,RequestContext
from django.core.urlresolvers import reverse
from django.views import generic
#from blog.models import Poll,Choice,Blog
from django import forms
from debateSNS.models import *
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib, time, random


'''def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': 1}
    return render(request, 'blog/index.html', context)
'''

def __checkin__(request):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')

def login(request):
    return render(request, 'blog/login.html' )

def logout(request):
    del request.session['username']
    return HttpResponseRedirect("login.html")

def loginCertifacate(request):
    if request.method == 'POST': 
    # If the form has been submitted...
        username = request.POST.get("username")
        tmpPassword = request.POST.get("password")
        md5Encode = hashlib.new("ripemd160")
        md5Encode.update(tmpPassword)
        password = md5Encode.hexdigest()

        admin = get_object_or_404(Admin, username=username)
        if admin.password == password:
            request.session['username'] = username
            return HttpResponseRedirect('/blog/article/show')
        else:
            return HttpResponse("密码错误") 
        

def contact(request):
    '''if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the previous section
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subject = {'data': 2}
            context = {'latest_poll_list': 1}
            return render(request, 'tt/index.html', {'data':2,
            											'bigcity':2})
            #return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })
    '''
    if request.method == 'POST':
        username = request.POST.get("username")
        request.session['username'] = data
        return HttpResponse(data)
        return render(request, 'blog/index.html', {'data':data,'bigcity':2})
    else:
        return HttpResponse(request.session['username'])

def addUserView(request):
    return render(request,"blog/addUserView.html")

def addUser(request):
    md5Encode = hashlib.new("ripemd160")
    username = request.POST.get("username")
    tmpPassword = request.POST.get("password")
    confirmPassword = request.POST.get("password2")
    if tmpPassword != confirmPassword:
        return HttpResponse("两次输入的密码不一致")
    md5Encode.update(tmpPassword)
    password = md5Encode.hexdigest()
    
    veryfyUser = Admin.objects.filter(username = username).all()
    
    try:
        HttpResponse(veryfyUser[0])
    except IndexError,e:
        veryfyUser = None
    if veryfyUser is not None:
        return HttpResponse("This user is already exits")

    admin = Admin(
        username = username,
        password = password
        )
    admin.save()
    return render(request,"blog/login.html")
 
def changePasswd(request):
    if request.method == "POST":
        username = request.POST.get("username")
        tmpPassword = request.POST.get("password")
        newPassword = request.POST.get("newPassword")
        md5Encode = hashlib.new("ripemd160")
        md5Encode.update(tmpPassword)
        password = md5Encode.hexdigest()

        user = get_object_or_404(User, username=username)
        if user.password == password:
            newEncode = hashlib.new("ripemd160")
            newEncode.update(newPassword)
            user.password = newEncode.hexdigest()
            user.save()
            del request.session['username']
            return HttpResponseRedirect("login.html")
        else:
            return HttpResponse("密码错误")    
        
    else:
        return render(request,"blog/changePasswd")

def index(request):
    return render(request,'blog/index2.html',{'news':News.objects.all()})
    return render(request,'blog/index2.html')


def generateInvitingCode(request):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')

    currentTime = time.time()
    md5Encode = hashlib.new("ripemd160")
    md5Encode.update(str(currentTime))
    invitingCode = md5Encode.hexdigest()
    newCode = InvitingCode(
        code = invitingCode,
        generate_user  =  request.session['username'],
        isUsed = 0
    )
    newCode.save()
    return HttpResponse(invitingCode)


########################################################
# this view is about the article 
# contains show article list , add article , change article, 
# delete article,and add new article
# News contain three parts , title content publish_time                 
########################################################

def article(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')

    if method == 'addArticle' :
        title = request.POST.get('title')
        content = request.POST.get('content')
        publish_time = datetime.datetime.now()
        author = request.session['username']
        introduction = request.POST.get('introduction')
        article = Article(
            title=title,
            content = content,
            publish_time = publish_time,
            author = author,
            introduction = introduction,
            )
        article.save()
        #Oid = news.id
        return HttpResponseRedirect('/blog/article/show')
    elif method == 'change':
        article = Article.objects.get(id=Oid)
        Article.date_format(article)
        #return HttpResponse(Oid)
        return render(request,'blog/changeArticle.html',{'article':article})
    elif method == 'save':
        if request.method == 'POST':
            article = {'id' : request.POST.get('id'),
                'title' : request.POST.get('title'),
                'content' : request.POST.get('content'),
                'publish_time' : request.POST.get('publish_time'),
                'introduction' : request.POST.get('introduction'),
                }

        Article.objects.filter(id=article['id']).update(content=article['content'],
                                                                                title = article['title'],
                                                                                publish_time = article['publish_time'],
                                                                                introduction = article['introduction'],
                                                                                )

        return HttpResponseRedirect('/blog/article/show')
    elif method == 'delete':
        Article.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request,'blog/addArticleView.html')
    elif method == 'show' or method == '':
        allArticle = Article.objects.all()
        for element in allArticle:
             Article.date_format(element)
        return render(request,'blog/showArticleList.html',{'article':allArticle})
    else:
        return HttpResponse('没有该方法')



########################################################
# this view is about the activity 
# contains show news list , add news , change news, 
# delete news,and add new news
# News contain three parts , title content date                 
########################################################


def activity(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')
    if method == 'addActivity':
        title = request.POST.get('title')
        introduction = request.POST.get('introduction')
        activity = Activity(
            title=title,
            time = datetime.datetime.now(),
            introduction = introduction,
            pulisher = request.session['username'],
            )
        activity.save()
        #return HttpResponse(activity.id)
        return HttpResponseRedirect('/blog/activity/show')
    elif method == 'change':
        return render(request,'blog/changeActivity.html',{'activity':Activity.objects.get(id=Oid)})

    elif method == 'save':
        if request.method == 'POST':
            activity = {'id' : request.POST.get('id'),
                'title' : request.POST.get('title'),
                'introduction' : request.POST.get('introduction'),
                }

        Activity.objects.filter(id=activity['id']).update(introduction=activity['introduction'],title=activity['title'])
        
        Oid = activity['id']
        return HttpResponse(str(activity))
        return HttpResponseRedirect('/blog/activity/show')

    elif method == 'delete':
        Activity.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request,'blog/addActivityView.html')
    elif method == 'show':
        return render(request,'blog/showActivityList.html',{'activity':Activity.objects.all()})
    else:
        return HttpResponse('没有该方法')




########################################################
# this view is about the us
# contains show news list , add  Us , change Us, 
# delete one,and add new one
# News contain three parts , title content date                 
########################################################

def us(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')
    if method == 'addUs':
        name = request.POST.get('name')
        description = request.POST.get('description')
        showOrder = request.POST.get('showOrder')
        blog_href = request.POST.get('blog_href')
        imageType = request.POST.get('type')
        '''save the imageFIle '''
        tmpImg = request.FILES['img']
        if tmpImg == None:
            return HttpResponse("Not upload a Image")
        imageName = initFileName()+'.'+imageType
        relativePath = "/files/images/"+imageName
        des_origin_path = settings.UPLOAD_PATH+'/images/'+imageName
        des_origin_f = open(des_origin_path, "ab") 
        
        for chunk in tmpImg.chunks():  
            des_origin_f.write(chunk)   
        des_origin_f.close() 
        img = Image(
            title = imageName,
            location = relativePath,
            uploadUser = request.session['username'],
            )
        img.save()
        '''save the info of the member'''
        member = Member(
            name=name,
            showOrder = int(showOrder),
            description = description,
            uploadUser = request.session['username'],
            image = relativePath,
            )
        member.save()
        #Oid = news.id
        return HttpResponseRedirect('/blog/us/show')
    elif method == 'change':
        return render(request,'blog/changeUs.html',{'member':Member.objects.get(id=Oid)})
    elif method == 'save':
        if request.method == 'POST':
            member = {'id' : request.POST.get('id'),
                    'name' : request.POST.get('name'),
                    'description' : request.POST.get('description'),
                    'showOrder': request.POST.get('showOrder'),
                    }
            Member.objects.filter(id=member['id']).update(description=member['description'],name=member['name'],showOrder=member['showOrder'])

        return HttpResponseRedirect('/blog/us/show')

    elif method == 'delete':
        Member.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request,'blog/addUsView.html')
    elif method == 'show':
        return render(request,'blog/showUsList.html',{'member':Member.objects.all()})
    else:
        return HttpResponse('没有该方法')


def plan(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')
    if method == 'addPlan':
        title = request.POST.get('title')
        content = request.POST.get('content')
        plan = Plan(
            title=title,
            content = content,
            uploadUser = request.session['username'],
            )
        plan.save()
        #Oid = news.id
        return HttpResponseRedirect('/blog/plan/show')
    elif method == 'change':
        return render(request,'blog/changePlan.html',{'plan':Plan.objects.get(id=Oid)})

    elif method == 'save':
        if request.method == 'POST':
            plan = {'id' : request.POST.get('id'),
                    'title' : request.POST.get('title'),
                    'content' : request.POST.get('content'),
                    }

            Plan.objects.filter(id=plan['id']).update(content=plan['content'])
            Plan.objects.filter(id=plan['id']).update(title=plan['title'])
            Oid = plan['id']
        return HttpResponseRedirect('/blog/plan/show')

    elif method == 'delete':
        Plan.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request,'blog/addPlanView.html')
    elif method == 'show':
        return render(request,'blog/showPlanList.html',{'plan':Plan.objects.all()})
    else:
        return HttpResponse('没有该方法')





########################################################
# this view is about the recruit
# contains show news list , add  Us , change Us, 
# delete one,and add new one
# News contain three parts , title content date                 
########################################################


def recruit(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')
    if method == 'addRecruit':
        title = request.POST.get('title')
        content = request.POST.get('content')
        recruit = Recruit(
            title=title,
            content = content,
            uploadUser = request.session['username'],
            )
        recruit.save()
        #Oid = news.id
        return HttpResponseRedirect('/blog/recruit/show')
    elif method == 'change':
        return render(request,'blog/changeRecruit.html',{'recruit':Recruit.objects.get(id=Oid)})
    elif method == 'save':
        if request.method == 'POST':
            recruit = {'id' : request.POST.get('id'),
                    'title' : request.POST.get('title'),
                    'content' : request.POST.get('content'),
                    }

            Recruit.objects.filter(id=recruit['id']).update(content=recruit['content'])
            Recruit.objects.filter(id=recruit['id']).update(title=recruit['title'])
            Oid = recruit['id']

        return HttpResponseRedirect('/blog/recruit/show')

    elif method == 'delete':
        Recruit.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request,'blog/addRecruitView.html')
    elif method == 'show':
       return render(request,'blog/showRecruitList.html',{'recruit':Recruit.objects.all()})

    else:
        return HttpResponse('没有该方法')


########################################################
# this view is about the contact
# contains show news list , add  Us , change Us, 
# delete one,and add new one
# News contain three parts , title content date                 
########################################################


def contact(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')
    if method == 'addContact':
        tel = request.POST.get('tel')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact = Contact(
            tel=tel,
            email = email,
            address = address,
            uploadUser = request.session['username'],
            )
        contact.save()
        return HttpResponseRedirect('/blog/contact/show')
    elif method == 'change':
        return render(request,'blog/changeContact.html',{'contact':Contact.objects.get(id=Oid)})
    elif method == 'save':
        if request.method == 'POST':
            contact = {'id' : request.POST.get('id'),
                    'title' : request.POST.get('title'),
                    'content' : request.POST.get('content'),
                    }

            Contact.objects.filter(id=contact['id']).update(content=contact['content'])
            Contact.objects.filter(id=contact['id']).update(title=contact['title'])
        return HttpResponseRedirect('/blog/contact/show')

    elif method == 'delete':
        Contact.objects.filter(id=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request,'blog/addContactView.html')
    elif method == 'show':
       return render(request,'blog/showContactList.html',{'contact':Contact.objects.all()})

    else:
        return HttpResponse('没有该方法')


##################################################################################################
#  file operation 
#   about image and video
##################################################################################################

def addImage(request):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')   
    if request.method == "POST":
        return HttpResponse(1)
    return render(request,'blog/addImage.html')

def addImageInfo(request):
    if request.method == "POST":
        des_origin_path = settings.UPLOAD_PATH+'/images/'+request.POST.get('title')
        des_origin_f = open(des_origin_path, "ab") 
        tmpImg = request.FILES['img']
        for chunk in tmpImg.chunks():  
            des_origin_f.write(chunk)   
        des_origin_f.close() 
        img = Image(
            title = request.POST.get('title'),
            location = des_origin_path,
            uploadUser = request.session['username'],
            )
        img.save()
        return HttpResponseRedirect('showImgList')
    return HttpResponse('allowed only via POST')

def showImgList(request):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')    
    return render(request,'blog/showImgList.html',{'image':Image.objects.all() })

def deleteImg(request,Oid):
    Image.objects.filter(id=Oid).delete()
    return HttpResponseRedirect('../showImgList')
def test(request):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    return   HttpResponse(BASE_DIR)

def initFileName():
    return hashlib.md5(str(random.random() + time.time())).hexdigest()
