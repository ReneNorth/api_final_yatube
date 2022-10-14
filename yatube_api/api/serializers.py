from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Group


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ['id', 'author', 'text', 'pub_date', 'image', 'group']
        model = Post
        read_only_fields = ('author', 'pub_date', 'author', 'id')
        extra_kwargs = {'text': {'required': True}}


class CommentsSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=Post.objects.all())
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', )
        extra_kwargs = {'text': {'required': True}}



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')