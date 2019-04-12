import json,random,datetime,pytz
from rest_framework.views import APIView
from django.http import JsonResponse
from api.models import Task,User,Childtask
from api.views.Validateview import Validate
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.core import serializers
from django.db.models import F,Q
from api.views.Datetimeview import get_current_time
#from django.utils import timezone

class Updatestatus(APIView):
	def post(self,request):
		request = request.data.get('update')
		requestobj = json.loads(request)
		if requestobj['userid'] and requestobj['authcode'] and requestobj['taskid']:
			valid_resp = self.check_customer_available(requestobj['userid'],requestobj['authcode'])
			if valid_resp['Status'] == 'Success':
				try:
					taskobj = Childtask.objects.get(userid=requestobj['userid'],childtask_id=requestobj['taskid'])

					taskupdate = self.update_task(requestobj['updatestatus'],requestobj)
					if taskupdate:
						resposnse = {"Status":"Success","Message":"Update Successfully","code":"200"}
					else:
						resposnse = {"Status":"Error","Message":"Task Not Update, Please Try Again","code":"100"}		
				except ObjectDoesNotExist:
					resposnse = {"Status":"Error","Message":"No Such Task Created","code":"100"}
			else:
				resposnse = valid_resp	
		else:
			resposnse = {"Status":"Error","Message":"Request Parameter is Missing","code":"100"}
		return JsonResponse(resposnse) 	

	def check_customer_available(self,userid,authcode):
		validateobj = Validate(userid,authcode)
		valid_resp = validateobj.check_customer_available()
		return valid_resp	

	def update_task(self,status,requestobj):
		if status == 'Completed':
			taskupdate = Childtask.objects.filter(
							Q(userid=requestobj['userid']) &
							Q(childtask_id=requestobj['taskid'])
						).update(status=requestobj['updatestatus'],completed_date = get_current_time())
		elif status == 'Remove':
			taskupdate = Childtask.objects.filter(
						Q(userid=requestobj['userid']) &
						Q(childtask_id=requestobj['taskid'])
					).update(status=requestobj['updatestatus'])
		elif status == 'Pending':
			taskupdate = Childtask.objects.filter(
							Q(userid=requestobj['userid']) &
							Q(childtask_id=requestobj['taskid'])
						).update(status=requestobj['updatestatus'])
		else:
			taskupdate = Childtask.objects.filter(
								Q(userid=requestobj['userid']) &
								Q(childtask_id=requestobj['taskid'])
				).update(status=requestobj['updatestatus'])
		return taskupdate	
				
						

class Createtask(APIView):
	def post(self,request):
		requestdata = request.data.get('createtask')
		requestobj = json.loads(requestdata)

		if requestobj['userid'] and requestobj['authcode'] and requestobj['foldername'] and requestobj['taskname'] and requestobj['schedule_date']:	
			valid_resp = self.check_customer_available(requestobj['userid'],requestobj['authcode'])
			if valid_resp['Status'] == 'Success':
				resposnse = self.create_new_task(requestobj)
			else:
				resposnse = valid_resp	
		else:
			resposnse = {"Status":"Error","Message":"Request Parameter is Missing","code":"100"}
		return JsonResponse(resposnse)	

	def create_new_task(self,requestobj):
		task_resp = self.check_parent_task_exist(requestobj)
		if task_resp['Status']=='Success':
			ptaskupdate = Task.objects.filter(
							Q(task_id=task_resp['taskid']) &
							Q(userid=requestobj['userid']) &
							Q(task_name=requestobj['foldername'])
						).update(status='pending')

			if ptaskupdate:
				resposnse =self.insert_new_task(task_resp['taskid'],requestobj)
			else:
				resposnse = {'Status':'Error','Message':'Please try Again','code':'100'}
		else:
			ptaskid = self.generate_task_id(7)
			ptaskobj = Task()
			ptaskobj.userid = requestobj['userid']
			ptaskobj.task_id	=ptaskid
			ptaskobj.task_name = requestobj['foldername']
			ptaskobj.created_date=get_current_time()
			ptaskobj.save()
			resposnse =	self.insert_new_task(ptaskid,requestobj)
		return resposnse	

	def check_parent_task_exist(self,requestobj):
		try:
			taskobj = Task.objects.get(
						Q(userid=requestobj['userid']) &
						Q(task_name=requestobj['foldername']) &
						~Q(status='Remove'))

			resposnse = {"Status":"Success","taskid":taskobj.task_id,"code":"200"}
		except ObjectDoesNotExist:
			resposnse = {"Status":"Error","code":"100"}
		return resposnse

	def insert_new_task(self,ptaskid,requestobj):
		childtaskobj,childtaskcreate = Childtask.objects.get_or_create(
				child_task_name=requestobj['taskname'],
				parent_task_id_id = ptaskid,
				status='Pending',
				defaults={
					'userid':requestobj['userid'],
					'childtask_id':int(self.generate_task_id(7)),
					'schedule_date':requestobj['schedule_date'],
					'created_date':get_current_time()
				}

			)
		if childtaskcreate:
			resposnse = {"Status":"Success","Message":"New Task Created","code":"200"}
		else:
			resposnse ={"Status":"Error","Message":"Task Already Available","code":"100"}
		return resposnse		

	def generate_task_id(self,length):
		taskid =''
		for i in range(0,length):
			taskid +=str(random.randint(1,9))
		return taskid	

	def check_customer_available(self,userid,authcode):
		validateobj = Validate(userid,authcode)
		valid_resp = validateobj.check_customer_available()
		return valid_resp	

class Fetchtask(APIView):
	def post(self,request):
		requestdata = request.data.get("fetch")
		requestobj = json.loads(requestdata)
		if requestobj['userid'] and requestobj['authcode']:
			valid_resp = self.check_customer_available(requestobj['userid'],requestobj['authcode'])
			if valid_resp['Status'] == 'Success':
				resposnse = self.fetch_task_list(requestobj)
			else:
				resposnse = valid_resp	
		else:
			resposnse = {"Status":"Error","Message":"Request Parameter is Missing","code":"100"}
		return JsonResponse(resposnse)

	def check_customer_available(self,userid,authcode):
		validateobj = Validate(userid,authcode)
		valid_resp = validateobj.check_customer_available()
		return valid_resp	

	def fetch_task_list(self,request):
		taskarr = []
		childtaskobj = Childtask.objects.select_related('parent_task_id').filter(userid=request['userid']).exclude(status='Remove')
		if len(childtaskobj):
			for obj in childtaskobj:
				taskobj = obj.parent_task_id
				fetch_resp = self.get_fetch_data(obj,taskobj,request['userid'])
				taskarr.append(fetch_resp)
			resposnse = {"Status":"Success","Message":"Ok","data":taskarr,"code":"200"}
		else:
			resposnse = {"Status":"Error","Message":"No Task Available","code":"100"}	
		return resposnse

	def get_fetch_data(self,childtaskobj,parentdata,userid):

		start_date = childtaskobj.created_date.strftime("%d-%m-%Y %H:%M:%S")
		schedule_date = childtaskobj.schedule_date.strftime("%d-%m-%Y %H:%M:%S")
		estimatedtl = self.get_differnece_time(start_date,schedule_date)

		if childtaskobj.completed_date:
			completedate = childtaskobj.completed_date.strftime("%d-%m-%Y %H:%M:%S")
			completed_dtl = self.get_differnece_time(start_date,completedate)
			completed_hrs =round(completed_dtl.seconds/3600)
			completed_days = completed_dtl.days
			completed_min = round(completed_dtl.seconds/60)
			completed_sec = round(completed_dtl.seconds)
		else:
			completed_hrs =0
			completed_days = 0
			completed_min = 0
			completed_sec =0

		fetcharr ={}
		fetcharr['userid']=	userid
		fetcharr['foldername'] = parentdata.task_name
		fetcharr['childtask_id'] = childtaskobj.childtask_id
		fetcharr['child_task_name'] = childtaskobj.child_task_name
		fetcharr['schedule_date'] = childtaskobj.schedule_date.strftime("%d-%m-%Y %H:%M:%S")
		fetcharr['created_date'] = childtaskobj.created_date.strftime("%d-%m-%Y %H:%M:%S")
		fetcharr['status'] = childtaskobj.status

		fetcharr['estimate_days'] = estimatedtl.days
		fetcharr['estimate_hrs'] = round(estimatedtl.seconds/3600)

		fetcharr['completed_days'] = completed_days
		fetcharr['completed_hrs'] = completed_hrs
		fetcharr['completed_min'] = completed_min
		fetcharr['completed_sec'] = completed_sec

		return fetcharr

	def get_differnece_time(self,date1,date2):
		time1 = datetime.datetime.strptime(date1,'%d-%m-%Y %H:%M:%S')
		time2 = datetime.datetime.strptime(date2,'%d-%m-%Y %H:%M:%S')
		diff_time = time2 - time1
		days = diff_time.days
		# hrs = round(diff_time.seconds/3600)
		# minute = round(diff_time.seconds/60)
		return diff_time

						
				
						
						

		
