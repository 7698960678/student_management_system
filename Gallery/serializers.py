from rest_framework import serializers
from .models import *

class ImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ["user" , "image" ,"id"]
        extra_kwargs={
            'image':{'read_only':True},
            'user':{'read_only':True},
            'id':{'read_only':True},
        }