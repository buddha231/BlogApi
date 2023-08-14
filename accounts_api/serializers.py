from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# from rest_framework.permissions import IsAuthenticated


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = ("id", "username", "email", "first_name", "last_name")
        read_only_fields = ["id"]
        extra_kwargs = {
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(), message="This email already exist!"
                    )
                ]
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

