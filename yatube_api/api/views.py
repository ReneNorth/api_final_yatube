from .serializers import PostSerializer, CommentsSerializer, GroupSerializer, FollowSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .pagination import PostsPaginator
from .permissions import PostsPermission, CommentsPermission
from posts.models import Post, Comment, Group, Follow
from rest_framework import viewsets, mixins, status, filters
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny


# import response

user_model = get_user_model()


class PostsViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    pagination_class = LimitOffsetPagination
    permissions_classes = [PostsPermission, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return [AllowAny(), ]
        elif self.action == 'destroy' or self.action == 'partial_update':
            return [PostsPermission(), ]
        else:
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


class GroupsRetreiveListViewSet(mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny, ]


class FollowGetPostViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ('following__username',) 
    
    def get_queryset(self):
        user = get_object_or_404(user_model, username=self.request.user)
        self.queryset = Follow.objects.filter(user_id=user.id)
        return self.queryset

    def perform_create(self, serializer):
        author_username = serializer.initial_data.get('following')
        author_id = user_model.objects.get(username=author_username).id
        serializer.save(user_id=self.request.user.id, following_id=author_id)
