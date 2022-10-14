from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField, PrimaryKeyRelatedField
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ['id', 'author', 'text', 'pub_date', 'image', 'group']
        model = Post
        read_only_fields = ('author', 'pub_date', 'id')
        extra_kwargs = {'text': {'required': True}}


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post')
        extra_kwargs = {'text': {'required': True}}


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(slug_field='username',
                                 queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ['user', 'following']
        read_only_fields = ['user', ]

    def validate(self, value):
        username = self.context['request'].user
        author = value.get('following')
        already_sub = Follow.objects.filter(user_id__username=username,
                                            following_id__username=author)
        if already_sub.exists():
            raise serializers.ValidationError(
                'Подписка уже существует'
            )
        elif username == author:
            raise serializers.ValidationError(
                'Зачем подисываться на себя?'
            )
        return value
