from django.contrib import admin
from .models import Post, UpVote, DownVote


# Register your models here.
admin.site.register(Post)

admin.site.register(UpVote)
admin.site.register(DownVote)