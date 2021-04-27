from django.db import models

# Create your models here.


class myusers(models.Model):
	myid = models.IntegerField(default=0)
	name = models.CharField(max_length=20)
	password = models.CharField(max_length=20)

class Question(models.Model): #database table represented by a class
	question_text = models.CharField(max_length=200) #/database field
	pub_date = models.DateTimeField('date published')

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)