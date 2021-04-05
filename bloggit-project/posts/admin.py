from django.contrib import admin
from .models import Post, Vote, UpVote, DownVote


# Register your models here.
admin.site.register(Post)
admin.site.register(Vote)
admin.site.register(UpVote)
admin.site.register(DownVote)