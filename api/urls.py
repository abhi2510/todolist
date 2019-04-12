from django.urls import path,include
from django.contrib import admin
from .views import Signup,login,Createtask,Fetchtask,Updatestatus,Updatescheduledate

urlpatterns = [
	path('/signup', Signup.as_view(),name='signup'),
	path('/login',login.as_view(),name='login'),
	path('/createtask',Createtask.as_view(),name='createtask'),
	path('/fetch',Fetchtask.as_view(),name='Fetchtask'),
	path('/update',Updatestatus.as_view(),name='Updatestatus'),
	path('/reschedule',Updatescheduledate.as_view(),name='reschedule'),
]