from re import sub

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic
from transliterate import translit

from components.make_url import make_url
from wall.forms import TopicForm, CommentForm, RegistrationForm
from wall.models import Topic, Comment, TopicLike


class IndexView(generic.ListView):
    def get_queryset(self):
        return Topic.objects.all()

    template_name = 'wall/index.html'
    context_object_name = 'topics'


def details(request, topic_url):
    topic = Topic.objects.get(url=topic_url)

    if request.method == "POST":
        is_liked = request.POST.get("like")
        if is_liked == 'liked' or is_liked == 'disliked':
            like = TopicLike.objects.get(topic=topic, creator=request.user)
            if like.is_active and is_liked == 'liked':
                like.is_active = False
                like.save()
            else:
                like.is_active = True
                like.save()
            return redirect('/topics/{}'.format(topic_url))
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.topic = topic
                comment.creator = request.user
                comment.save()
            return redirect('/topics/{}'.format(topic_url))
    form = CommentForm()
    try:
        like = TopicLike.objects.get(topic=topic, creator=request.user)
    except ObjectDoesNotExist:
        like = TopicLike()
        like.creator = request.user
        like.topic = topic
        like.save()
    return render(request, "wall/topic.html",
                  {"form": form, "topic": topic, "comments": Comment.objects.filter(topic=topic), "like": like})


def create_new_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.url = make_url(topic.title)
            topic.creator = request.user
            topic.save()
            return redirect('/topics/{}'.format(topic.url))
    else:
        form = TopicForm()
    return render(request, 'wall/create_new_topic.html', {'form': form})


def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'],
                                                first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'],
                                                email=request.POST['email'])
                user.save()
                return redirect("/auth/")
        form = RegistrationForm()
        return render(request, 'wall/registration.html', {'form': form})
    else:
        return HttpResponse("You've already logged in")


def auth(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
        return render(request, 'wall/auth.html')
    else:
        return HttpResponse("You've already logged in")
