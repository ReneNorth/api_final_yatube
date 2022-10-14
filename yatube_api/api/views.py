from .serializers import PostSerializer, CommentsSerializer, GroupSerializer
from django.shortcuts import get_object_or_404
from .pagination import PostsPaginator
from .permissions import PostsPermission, CommentsPermission
from posts.models import Post, Comment, Group
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

# import response


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
            
    # def destroy(self, request, **kwargs):
    #     post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
    #     print(self.check_object_permissions(request, post))
    #     self.check_object_permissions(request, post)
    #     post.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
    # def partial_update(self, serializer, **kwargs):
    #     post = get_object_or_404(Post, pk=self.kwargs.get('id'))
    #     # self.check_object_permissions(self.request, post)
    #     serializer.save(post=post)
        # send_email_confirmation(user=self.request.user, modified=instance)
        
        
        # post = get_object_or_404(Post, pk=self.kwargs.get('id'))
        # serializer = PostSerializer(post, data=request.data)
        # self.check_object_permissions(self.request, post)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data,
        #                     status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_403_FORBIDDEN)


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
