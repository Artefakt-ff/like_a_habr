from django.conf.urls import url

from api.views import AuthView, TopicView, CommentView

urlpatterns = [
    url(r'^comment\.(?P<action>[a-z]+)', CommentView.as_view(), name='comment'),
    url(r'^topic\.(?P<action>[a-z]+)', TopicView.as_view(), name='topic'),
    url(r'^auth\.(?P<action>[a-z]+)', AuthView.as_view(), name='auth'),
]