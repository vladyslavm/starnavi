from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from rest_framework import generics, permissions, mixins, status
from .models import Post, UpVote, DownVote
from .serializers import PostSerializer, UpVoteSerializer, DownVoteSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
import datetime



@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)            
            return JsonResponse({'token':str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error':'The username has already been taken'}, status=400)


@csrf_exempt
def analytics(request):
    
    serializer_class = UpVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    data = JSONParser().parse(request)

    date_to = data['date_to']
    date_from = data['date_from']

    q1 = UpVote.objects.all()

    q2 = q1.exclude(created__gte=date_to)

    q3 = q2.filter(created__gte=date_from)

    a = {}

    for i in q3:

        print("vote: " + str(i.id) + ", added on " + str(i.created))


    return HttpResponse(q2)


    # return JsonResponse({'error':'The username has already been taken'}, status=200)




class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(poster=self.request.user)



class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'], poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('This is not your post')



class UpVoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    
    serializer_class = UpVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        post = Post.objects.get(pk=self.kwargs['pk'])

        return UpVote.objects.filter(voter=user, post=post)


    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))


    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            raise ValidationError('No votes here')



class DownVoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    
    serializer_class = DownVoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        post = Post.objects.get(pk=self.kwargs['pk'])

        return DownVote.objects.filter(voter=user, post=post)


    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted')
        serializer.save(voter=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))


    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            raise ValidationError('No votes here')



