from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny

from accounts_api.serializers import UserSerializer


class UserRecordView(generics.GenericAPIView):
    """API View to create or get user info.
    a POST request allows to create a new user.
    """
    serializer_class = UserSerializer

    def get(self, format=None):
        """make get request with token present in the authentication header
        to get user info"""
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)

    def post(self, request):
        permission_classes = [AllowAny]
        """make post request with user info to register"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            instance = serializer.create(validated_data=request.data)
            response_data = serializer.data
            response_data['id'] = instance.id
            return Response(
                response_data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def put(self, request):
        """make put request with user info to register"""
        user = self.request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.save(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request):
        """make delete request with user info to register"""
        user = self.request.user
        user.delete()
        return Response(
            {
                "error": False,
                "error_msg": "User deleted successfully",
            },
            status=status.HTTP_200_OK,
        )
