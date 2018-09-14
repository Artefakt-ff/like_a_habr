from django.contrib.auth.models import User
from django.forms import ModelForm

from wall.models import Topic, Comment, TopicLike


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'body']


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class AuthForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

