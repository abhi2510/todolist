import requests,json,datetime
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from api.views.Datetimeview import get_current_time

# Create your views here.
def login(request):
	return render(request,'login.html')	

def signup(request):
	return render(request,'signup.html')	

def logout(request):
	try:
		del request.session['authcode']
		del request.session['userid']
		del request.session['lastlogin']
	except:
		pass	
	return redirect('http://127.0.0.1:8000/web/')	

def createtask(request,id=None):

	if check_session_detail(request):

		if check_session_expired(request.session['lastlogin']):

			data = json.dumps({"userid":request.session['userid'],"authcode":request.session['authcode']})
			payload = {'fetch':data}
			url = 'http://127.0.0.1:8000/api/fetch'
			response = call_request_api(url,payload)
			if response['Status'] == 'Success':
				return render(request,'create_task.html',{'tasklist':response['data'],'count':1,'userid':request.session['userid'],'authcode':request.session['authcode']})
			else:
				return render(request,'create_task.html',{'tasklist':0,'count':0,'userid':id,'authcode':request.session['authcode']})
		else:
			del request.session['authcode']
			del request.session['userid']
			del request.session['lastlogin']
			return redirect('http://127.0.0.1:8000/web/')		
	else:
		return redirect('http://127.0.0.1:8000/web/')

def call_request_api(url,requestdata):
	response = requests.post(url,data=requestdata)
	response = response.text
	response = json.loads(response)
	return response

def check_session_detail(request):
	if request.session.has_key('userid') and request.session.has_key('authcode') and request.session.has_key('lastlogin'):
		return True
	else:
		return False	

def check_session_expired(lastlogin):
	todaydatetime =	get_current_time()
	lastlogin = datetime.datetime.strptime(lastlogin,"%Y-%m-%d %H:%M:%S")
	time_diff = todaydatetime-lastlogin
	if time_diff.seconds >= 3600:
		return False
	else:
		return True	

