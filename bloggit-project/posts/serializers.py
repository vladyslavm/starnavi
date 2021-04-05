from rest_framework import serializers
from .models import Post, UpVote, DownVote


class PostSerializer(serializers.ModelSerializer):

    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    score = serializers.SerializerMethodField()
    upvotes = serializers.SerializerMethodField()
    dnvotes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'poster', 'poster_id', 'created', 'score', 'upvotes', 'dnvotes']


    def get_upvotes(self, post):
        return UpVote.objects.filter(post=post).count()

    def get_dnvotes(self, post):
        return DownVote.objects.filter(post=post).count()

    def get_score(self, post):
        upvotes = UpVote.objects.filter(post=post).count()
        dnvotes = DownVote.objects.filter(post=post).count()
        return str(upvotes-dnvotes)#Vote.objects.filter(post=post).count()


class UpVoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpVote
        fields = ['id']


class DownVoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = DownVote
        fields = ['id']