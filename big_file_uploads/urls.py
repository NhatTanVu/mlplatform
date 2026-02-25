from django.urls import path
from . import views

urlpatterns = [
    path("api/upload/request-url", views.request_upload_url),
    path("api/upload/confirm", views.confirm_upload),
    path("", views.upload_page, name="upload")
]