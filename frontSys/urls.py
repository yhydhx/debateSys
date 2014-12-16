from django.conf.urls import patterns, url

from frontSys import views

urlpatterns = patterns('',
    url(r'^index\.html$', views.fsIndex, name = "Index"),
    url(r'^member\.html$', views.fsMember, name = "member"),
    url(r'^article\.html$', views.fsArticle, name = "article"),
    url(r'^register\.html$', views.register, name = "register"),
    url(r'^loginCertificate$', views.loginCertificate, name = "loginCertificate"),
    url(r'^addUser$', views.addUser, name = "addUser"),
)
