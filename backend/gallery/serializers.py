from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Picture


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
