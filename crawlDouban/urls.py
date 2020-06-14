from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('search/',views.search,name="search"),
    path('hot/',views.hot,name="hot"),
    path('recommend/',views.recommend,name="recommend"),
    path('craw/',views.craw,name="craw"),
    path('wordCould/',views.wordCould,name="wordCould"),
    path('getImage/',views.getImage,name="getImage"),
    path('getcomment/',views.getcomment,name="getcomment"),
    path('admin/',views.admin,name="admin"),

]
urlpatterns += staticfiles_urlpatterns()