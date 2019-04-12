from django.db import models

class Task(models.Model):
	userid = models.BigIntegerField()
	task_id = models.BigIntegerField(primary_key=True)
	task_name = models.CharField(max_length=300)
	status = models.CharField(max_length=100,default='Pending')
	created_date = models.DateTimeField(null=True)

	def __unicode__(self):
		return self.task_name


class Childtask(models.Model):
	userid = models.BigIntegerField()
	parent_task_id = models.ForeignKey(Task,on_delete=models.CASCADE)
	childtask_id = models.BigIntegerField()
	child_task_name = models.CharField(max_length=200)
	schedule_date = models.DateTimeField(null=True)
	status = models.CharField(max_length=100,default='Pending')
	completed_date = models.DateTimeField(null=True)
	created_date = models.DateTimeField(null=True)

	def __unicode__(self):
		return self.child_task_name
