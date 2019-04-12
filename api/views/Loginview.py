import json,datetime
from rest_framework.views import APIView
from django.http import JsonResponse
from api.models import User
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from api.views.key import Key
from api.views.Datetimeview import get_current_time

class login(APIView):
	def post(self,request):
		requestdata = request.data.get('login')
		requestobj = json.loads(requestdata)
		if requestobj['email'] and requestobj['password']:
			lastlogin_date = get_current_time()
			user_exist_resp = self.check_user_exist(requestobj['email'],requestobj['password'],lastlogin_date)
			if user_exist_resp['Status'] == 'Success':
				request.session['userid'] = user_exist_resp['user_id']
				request.session['authcode'] = user_exist_resp['authcode']
				request.session['lastlogin'] = lastlogin_date.strftime("%Y-%m-%d %H:%M:%S")
				response = {"Status":"Success","Message":"Login Successfully","userid":user_exist_resp['user_id'],"code":"200"}
			else:
				response = user_exist_resp	
		else:
			response = {'Status':'Error','Message':'Request Parameter is Missing','code':'100'}
		return JsonResponse(response)

	def check_user_exist(self,*args):
		try:
			userobj = User.objects.get(email=args[0])
			keyobj = Key()
			if userobj.password == keyobj.encrypt_data(args[1]):
				userobj.last_login = args[2]
				userobj.save()
				response = {'Status':'Success','Message':'Ok','user_id':userobj.userid,'authcode':userobj.salt,'code':'200'}
			else:
				response ={'Status':'Error','Message':'Invalid password','code':'100'}	
		except ObjectDoesNotExist:
			response = {'Status':'Error','Message':'Invalid Email','code':'100'}
		return response	

