from django.db import models

class UserManager(models.Manager):
	def get_querysett(self):
		return super().get_queryseet()

class User(models.Model):
	userid = models.BigIntegerField(primary_key=True)
	username = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	phone_number = models.BigIntegerField(null=True)
	salt = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	status =models.BooleanField(default=1)
	registered_date = models.DateTimeField(null=True)
	last_login=models.DateTimeField(null=True)

	objects = models.Manager()
	email_check = UserManager()

	def __unicode__(self):
		return self.username