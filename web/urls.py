from django.urls import path,include
from django.contrib import admin
from .views import login,signup,createtask,logout

urlpatterns = [
	path('/',login,name='login'),
	path('/login',login,name='login'),
	path('/signup',signup,name='signup'),
	path('/createtask/<int:id>',createtask,name='createtask'),
	path('/logout',logout,name='logout'),
]