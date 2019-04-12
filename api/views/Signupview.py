import json,random,hashlib
import datetime
from rest_framework.views import APIView
from django.http import JsonResponse
from api.models import User
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from api.views.key import Key
from api.views.Datetimeview import get_current_time



class Signup(APIView):
	def post(self,request):
		requestdata = request.data.get('signup')
		requestobj = json.loads(requestdata)
		if requestobj['usename'] and requestobj['email'] and requestobj['password'] and requestobj['number']:
			check_resp =self.check_already_registered(requestobj['email'],requestobj['number'])
			if check_resp['Status'] == 'Success':
				userid,authcode=self.user_register(requestobj)
				lastlogin_date = get_current_time()
				request.session['userid'] = userid
				request.session['authcode'] = authcode
				request.session['lastlogin'] = lastlogin_date.strftime("%Y-%m-%d %H:%M:%S")
				response = {'Status':'Success','Message':'Register Successfully','userid':userid,'code':'200'}
			else:
				response = check_resp
		else:
			response = {'Status':'Error','Message':'Request Parameter is Missing','code':'300'}	
		return JsonResponse(response)

	def check_already_registered(self,*args):
		useremailobj = User.objects.filter(email=args[0]).count()
		usernumnerobj = User.objects.filter(phone_number=args[1]).count()
		if useremailobj:
			response ={"Status":"Error","Message":"Email is Already Registered","code":"100"}
		elif usernumnerobj:
			response = {"Status":"Error","Message":"Number is Already Registered","code":"100"}
		else:
			response ={"Status":"Success","Message":"Ok","code":"100"}
		return response

	def user_register(self,requestobj):
		keyobj = Key()

		userid = self.generate_random_nbr(5)
		authcode = keyobj.encrypt_data(userid)
		user = User()
		user.userid = userid
		user.username = requestobj['usename']
		user.email = requestobj['email']
		user.phone_number = requestobj['number']
		user.salt = authcode
		user.password = keyobj.encrypt_data(requestobj['password'])
		user.registered_date = get_current_time()
		user.last_login =get_current_time()

		user.save()

		return userid,authcode
 
	
	def generate_random_nbr(self,length):
		nbr =''
		for i in range(0,length):
			nbr = nbr+str(random.randint(1,9))
		return nbr

		

		

