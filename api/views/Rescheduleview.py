import json
from rest_framework.views import APIView
from django.http import JsonResponse
from api.views.Validateview import Validate
from django.core.exceptions import ObjectDoesNotExist
from api.models import Reschedule,Childtask
import datetime

class Updatescheduledate(APIView):
	def post(self,request):
		requestdata = request.data.get('reschedule')
		requestobj = json.loads(requestdata)

		if requestobj['userid'] and requestobj['authcode'] and requestobj['taskid']:
			valid_resp = self.check_customer_available(requestobj['userid'],requestobj['authcode'])
			if valid_resp['Status'] == 'Success':
				try:
					childtaskobj = Childtask.objects.get(childtask_id=requestobj['taskid'],status='pending')
					new_schedule_date = self.insert_reschedule_detail(requestobj['userid'],requestobj['taskid'],childtaskobj)
					childtaskobj.schedule_date = new_schedule_date
					childtaskobj.save()
					response = {"Status":"Success","Message":"Ok","code":"200"}
				except ObjectDoesNotExist:
					response = {"Status":"Error","Message":"No Such TaskID Available","code":"100"}
			else:
				response = valid_resp	
		else:
			response = {"Status":"Error","Message":"Request Parameter is Missing","code":"100"}
		return JsonResponse(response)	

	def check_customer_available(self,userid,authcode):
		validateobj = Validate(userid,authcode)
		valid_resp = validateobj.check_customer_available()
		return valid_resp	


	def insert_reschedule_detail(self,userid,taskid,childtaskobj):
		rescheduleobj = Reschedule()
		new_schedule_date = childtaskobj.schedule_date +datetime.timedelta(hours=2)
		rescheduleobj.userid = userid
		rescheduleobj.taskid = taskid
		rescheduleobj.schedule_date = childtaskobj.schedule_date
		rescheduleobj.re_schedule_date = new_schedule_date
		rescheduleobj.save()
		return new_schedule_date
