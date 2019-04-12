import json
from django.http import JsonResponse
from api.models import User
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned

class Validate:
	def __init__(self,userid=None,salt=None):
		self.userid = userid
		self.authcode = salt

	def check_customer_available(self):
		try:
			userdata = User.objects.get(userid=self.userid)
			if userdata.salt == self.authcode:
				response = {"Status":"Success","Message":"ok","code":"200"}
			else:
				response = {"Status":"Error","Message":"Invalid Authcode","code":"100"}	
		except	ObjectDoesNotExist:
			response = {"Status":"Error","Message":"No User Available","code":"100"}
		except MultipleObjectsReturned:
			response = {"Status":"Error","Message":"Multiple Same User Available","code":"100"}	
		return response

