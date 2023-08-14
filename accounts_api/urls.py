from django.urls import path
from .views import UserRecordView

urlpatterns = [
    path("users/", UserRecordView.as_view(), name="user-list"),  # GET (list) and POST
]
