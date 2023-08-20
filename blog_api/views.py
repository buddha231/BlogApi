from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import BlogSerializer
from .models import Blog

from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.exceptions import PermissionDenied


class BlogView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.all()

    def perform_destroy(self, instance):

        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own blog")
        instance.delete()

    def perform_update(self, instance):
        test_instance = self.get_serializer(instance)
        if test_instance.author != self.request.user:
            raise PermissionDenied("You can only update your own blog")
        instance.save()


class BlogCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogSelfView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    def get_queryset(self):
        user = self.request.user
        return user.blogs.all()


class BlogLikeView(APIView):
    def get(self, request, pk):
        blog = Blog.objects.get(id=pk)
        user = request.user
        like_users = blog.like_users.all()
        if user in like_users:
            blog.like_users.remove(user)
            return Response(
                {
                    "error": False,
                    "error_msg": "Blog unliked successfully",
                    "like_count": len(like_users) - 1,
                },
                status=status.HTTP_200_OK,
            )
        else:
            blog.like_users.add(user)
            return Response(
                {
                    "error": False,
                    "error_msg": "Blog liked successfully",
                    "like_count": len(like_users) + 1,
                },
                status=status.HTTP_200_OK,
            )
