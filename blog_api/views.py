from rest_framework import generics
from rest_framework.permissions import  IsAuthenticated, AllowAny

from .serializers import BlogSerializer
from .models import Blog

from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.exceptions import PermissionDenied


# class BlogView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         if not request.user.is_authenticated:
#             return Response(
#                 {
#                     "error": True,
#                     "error_msg": "You must be logged in to create a blog",
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
#         serializer = BlogSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=ValueError):
#             serializer.save(author=self.request.user)
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(
#             {
#                 "error": True,
#                 "error_msg": serializer.error_messages,
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#
#     def get(self, request, pk=None):
#         if pk:
#             blog = Blog.objects.get(id=pk)
#             serializer = BlogSerializer(blog)
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_200_OK,
#             )
#         blogs = Blog.objects.all()
#         serializer = BlogSerializer(blogs, many=True)
#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK,
#         )
#
#     def put(self, request, pk):
#         if not request.user.is_authenticated:
#             return Response(
#                 {
#                     "error": True,
#                     "error_msg": "You must be logged in to update a blog",
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
#         blog = Blog.objects.get(id=pk)
#         if blog.author != request.user:
#             return Response(
#                 {
#                     "error": True,
#                     "error_msg": "You can only update your own blog",
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
#         serializer = BlogSerializer(blog, data=request.data)
#         if serializer.is_valid(raise_exception=ValueError):
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_200_OK,
#             )
#         return Response(
#             {
#                 "error": True,
#                 "error_msg": serializer.error_messages,
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#
#     def delete(self, request, pk):
#         if not request.user.is_authenticated:
#             return Response(
#                 {
#                     "error": True,
#                     "error_msg": "You must be logged in to delete a blog",
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
#         blog = Blog.objects.get(id=pk)
#         if blog.author != request.user:
#             return Response(
#                 {
#                     "error": True,
#                     "error_msg": "You can only delete your own blog",
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )
#         blog.delete()
#         return Response(
#             {
#                 "error": False,
#                 "error_msg": "Blog deleted successfully",
#             },
#             status=status.HTTP_200_OK,
#         )
#
class BlogView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    queryset = Blog.objects.all()

    def perform_destroy(self, instance):
        print(f"{instance=} {self.request.user=}")
        if instance.author != self.request.user:
            raise PermissionDenied
            return Response(
                {
                    "error": True,
                    "error_msg": "You can only delete your own blog",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            instance.delete()
            return Response(
                {
                    "error": False,
                    "error_msg": "Blog deleted successfully",
                },
                status=status.HTTP_200_OK,
            )


class BlogCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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

