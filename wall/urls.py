from django.conf.urls import url

from wall.views import IndexView, details, create_new_topic, registration, auth

urlpatterns = [
    url(r'^topics/(?P<topic_url>([a-z]|[0-9]|_|-)+$)', details, name='details'),
    url(r'^create_new_topic/$', create_new_topic, name='create_new_topic'),
    url(r'^auth/$', auth, name='auth'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^$', IndexView.as_view(), name='index')
]