from django.db import models

class Reschedule(models.Model):
	userid = models.BigIntegerField()
	taskid = models.BigIntegerField(null=True)
	schedule_date = models.DateTimeField(null=True)
	re_schedule_date = models.DateTimeField(null=True)
	created_date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.taskid

	class Meta:
		db_table ='reschedule'