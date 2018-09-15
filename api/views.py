from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import TopicSerializer, CommentSerializer, LikeSerializer
from components.check_like import check_like
from components.make_limit_and_offset import make_limit_and_offset
from components.make_url import make_url
from wall.forms import TopicForm, CommentForm
from wall.models import Topic, Comment


class AuthView(APIView):
    def post(self, request, action, format=None):
        if action == 'login':
            if request.user.is_authenticated:
                return Response({'details': 'User already have been authenticated'},
                                status=status.HTTP_200_OK)
            else:
                try:
                    username = request.data['username']
                    password = request.data['password']
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return Response({'details': 'User is authenticated'}, status=status.HTTP_200_OK)
                    return Response({'errors': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
                except KeyError:
                    return Response({'errors': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
        elif action == 'logout':
            if not request.user.is_authenticated:
                return Response({'errors': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
            logout(request)
            return Response({'details': 'Logout'}, status=status.HTTP_200_OK)


class TopicView(APIView):
    def get(self, request, action, format=None):
        if action == 'list':
            limit, offset = make_limit_and_offset(request.GET)
            topics = Topic.objects.order_by('-created')[offset:limit]
            serializer = TopicSerializer(topics, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, action, format=None):
        if action == 'create':
            if request.user.is_authenticated:
                form = TopicForm(request.data)
                if form.is_valid():
                    topic = form.save(commit=False)
                    topic.url = make_url(topic.title)
                    topic.creator = request.user
                    topic.save()
                    serializer = TopicSerializer(topic)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        elif action == 'like':
            if request.user.is_authenticated:
                topic_id = request.data.get('topic_id')
                try:
                    topic = Topic.objects.get(id=topic_id)
                    if topic is not None:
                        like = check_like(user=request.user, topic=topic)
                        if like:
                            like.save()
                        else:
                            return Response({'errors': 'Can not remove like'}, status=status.HTTP_403_FORBIDDEN)
                        serializer = LikeSerializer(like)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    return Response({"errors": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentView(APIView):
    def get(self, request, action, format=None):
        if action == 'list':
            topic_id = request.GET.get('topic_id')
            limit, offset = make_limit_and_offset(request.GET)
            try:
                topic = Topic.objects.get(id=topic_id)
                comments = Comment.objects.filter(topic=topic).order_by("-created")[offset:limit]
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({"errors": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, action, format=None):
        if request.user.is_authenticated:
            try:
                topic_id = request.data.get('topic_id')
                print(topic_id)
                topic = Topic.objects.get(id=topic_id)
                form = CommentForm(request.data)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.creator = request.user
                    comment.topic = topic
                    comment.save()
                    serializer = CommentSerializer(comment)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({"errors": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
