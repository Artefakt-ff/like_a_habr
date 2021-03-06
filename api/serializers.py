from rest_framework import serializers

from wall.models import Topic, Comment, TopicLike


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'body', 'url', 'number_of_comments', 'number_of_likes', 'creator', 'created']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created', 'topic', 'creator']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicLike
        fields = ['topic', 'creator', 'is_active']
