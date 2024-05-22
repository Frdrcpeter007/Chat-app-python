from django.conf import settings
from rest_framework import serializers

from .models import Category, Server


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# class OwnerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = settings.AUTH_USER_MODEL
#         fields = ['id', 'username']

class ServerSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    # owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Server
        fields = '__all__'