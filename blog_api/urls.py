from django.urls import path

from .views import BlogView, BlogCreateView, BlogSelfView, BlogLikeView

urlpatterns = [
    path("", BlogCreateView.as_view()),
    path("self/", BlogSelfView.as_view()),
    path("<int:pk>/", BlogView.as_view()),
    path("<int:pk>/like/", BlogLikeView.as_view()),
]
