from django.urls import path
from .views import *

urlpatterns = [
    path('image',ImageUploadView.as_view(),name='Image-Upload'),
    path('image/list',ImageListView.as_view(),name='Image-List'),
]