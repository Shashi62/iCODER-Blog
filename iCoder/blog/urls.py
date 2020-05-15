# cmd /c "e:\Python\Blog\iCoder\SBKProjectenv\Scripts\deactivate.bat"
# cmd /c "e:\Python\Blog\iCoder\SBKProjectenv\Scripts\activate.bat"

from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    # API to post a comment
    path('postComment', views.postComment, name='postComment'),
    
    path('', views.blogHome, name='blogHome'),
    path('<str:slug>', views.blogPost, name='blogPost'),

]
