from rest_framework import serializers
from rest_framework.permissions import AllowAny

from .models import Blog
from accounts_api.serializers import UserSerializer


class BlogSerializer(serializers.ModelSerializer):
    """Serializer for Blog model"""

    permission_classes = [AllowAny]
    author = UserSerializer(read_only=True)
    like_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Blog
        fields = ("id", "title", "description",
                  "photo", "author", "like_users", "date")
        read_only_fields = ["author", "like_users"]
        # depth = 1
