from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentsRetDelPatchViewSet, FollowGetPostViewSet,
                    GroupsRetreiveListViewSet, PostsViewSet)

router = DefaultRouter()
router.register(r'posts', PostsViewSet)
router.register(r'groups', GroupsRetreiveListViewSet)
router.register(r'posts/(?P<id>\d+)/comments', CommentsRetDelPatchViewSet)
router.register(r'follow', FollowGetPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
