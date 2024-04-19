from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Post, Comment
from myauth.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content' , 'date_created' , 'category', 'author']
        extra_kwargs = {'date_created': {'read_only': True},
                        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            category_instance = Category.objects.get(pk=data['category'])
            category_serializer = CategorySerializer(category_instance)
            data['category'] = category_serializer.data
        return data
        

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content' , 'author' , 'date_created' , 'post']
        extra_kwargs = {'date_created': {'read_only': True},
                        }
