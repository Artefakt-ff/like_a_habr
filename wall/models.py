import datetime
from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    title = models.CharField(default='Empty Title', max_length=100)
    body = models.TextField()
    url = models.CharField(auto_created=True, max_length=50, default='default_url')
    number_of_comments = models.IntegerField(default=0, auto_created=True)
    number_of_likes = models.IntegerField(default=0, auto_created=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='pub_date', auto_created=True, default=datetime.datetime.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    def __str__(self):
        return self.topic.title

    body = models.TextField(max_length=200)
    created = models.DateTimeField(verbose_name='pub_date', auto_created=True, default=datetime.datetime.now)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class TopicLike(models.Model):
    def __str__(self):
        return self.topic.title
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    liked = models.DateTimeField(auto_created=True, default=datetime.datetime.now)
