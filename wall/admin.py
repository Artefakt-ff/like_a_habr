from django.contrib import admin

from wall.models import Topic, TopicLike, Comment

admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(TopicLike)
