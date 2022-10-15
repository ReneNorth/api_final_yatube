from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from posts.models import Comment, Follow, Group, Post
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import CommentsPermission, PostsPermission
from .serializers import (CommentsSerializer, FollowSerializer,
                          GroupSerializer, PostSerializer)

User = get_user_model()


class PostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permissions_classes = [PostsPermission, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'destroy' or self.action == 'partial_update':
            return [PostsPermission(), ]
        return super().get_permissions()


class CommentsRetDelPatchViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [CommentsPermission, ]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('id'))
        self.queryset = Comment.objects.filter(post_id=post.id)
        return self.queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        serializer.save(author=self.request.user, post=post)


class GroupsRetreiveListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowGetPostViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ('following__username',)
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        self.queryset = Follow.objects.filter(user_id=user.id)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
