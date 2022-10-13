from .serializers import PostSerializer, CommentSerializer
from posts.models import Post, Comment
from rest_framework import viewsets
from rest_framework.response import Response

# import response


class PostsViewSet(viewsets.ModelViewSet):
    serializer = PostSerializer
    queryset = Post.objects.all()
