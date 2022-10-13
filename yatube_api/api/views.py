from .serializers import PostSerializer, CommentSerializer
from .pagination import PostsPaginator
from posts.models import Post, Comment
from rest_framework import viewsets
from rest_framework.response import Response

# import response


class PostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = PostsPaginator

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
