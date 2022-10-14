from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (PostsViewSet,
                    CommentsRetDelPatchViewSet,
                    GroupsRetreiveListViewSet,
                    FollowGetPostViewSet)

router = DefaultRouter()
router.register(r'posts', PostsViewSet)
router.register(r'groups', GroupsRetreiveListViewSet)
router.register(r'posts/(?P<id>\d+)/comments', CommentsRetDelPatchViewSet)
router.register(r'follow', FollowGetPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
