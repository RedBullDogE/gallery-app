from rest_framework import serializers

from .models import Picture
from django.contrib.auth import get_user_model

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = '__all__'
class PictureDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Picture
        fields = '__all__'


class PictureListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Picture
        fields = ['id', 'author', 'file']
