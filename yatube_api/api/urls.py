from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentsRetDelPatchViewSet, FollowGetPostViewSet,
                    GroupsRetreiveListViewSet, PostsViewSet)

router = DefaultRouter()
router.register('posts', PostsViewSet)
router.register('groups', GroupsRetreiveListViewSet)
router.register(r'posts/(?P<id>\d+)/comments', CommentsRetDelPatchViewSet)
router.register('follow', FollowGetPostViewSet, basename='followers')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
