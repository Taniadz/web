from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by(-added_at)
    def popular(self):
        return self.order_by(rating)

class Question(models.Model):
    title = models.CharField(max_length=125)
    text = models.TextField()
    added_at = models.DateField(blank = True, auto_now_add=True)
    rating = models.IntegerField(default = 0)
    author = models.ForeignKey(User,default=1)
    likes = models.ManyToManyField(User, related_name='question_like_user')
    objects=QuestionManager()
    
    def __unicode__(self):
        return self.title

    def get_url(self):
	return reverse('one_question',
	    kwargs={'pk': self.pk})

class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateField(blank = True, auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, default=1)

    def __unicode__(self):
        return self.text
  
    def get_url(self):
	return reverse('one_question',
	    kwargs={'pk': self.pk})