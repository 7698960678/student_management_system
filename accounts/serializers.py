from rest_framework import serializers
from .models import *
from rest_framework.authtoken.models import Token

### User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__' 
        fields = [ 'email', 'is_admin', 'is_teacher','is_student']

### Login Serializer
class LoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class AdminSignupSerializer(serializers.ModelSerializer):
    ## Token
    class Meta:
        model = Token
        fields = "__all__"
    ## User
    class Meta:
        model=User
        fields=['email','password','username','phone_number']
    def save(self, **kwargs):
        user=User(
            email=self.validated_data['email']
        )
        user.set_password(self.validated_data['password'])
        user.is_admin=True
        user.username=self.validated_data['username']
        user.phone_number=self.validated_data['phone_number']
        user.save()
        token = Token.objects.get(user=user)
        Admin.objects.create(user=user, token=token,)
        return user

class TeacherSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"
    class Meta:
        model=User
        fields=['email','password','username','phone_number']
    def save(self, **kwargs):
        user=User(
            email=self.validated_data['email']
        )
        user.set_password(self.validated_data['password'])
        user.is_teacher=True
        user.username=self.validated_data['username']
        user.phone_number=self.validated_data['phone_number']
        user.save()
        return user

class StudentSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"
    class Meta:
        model=User
        fields=['email','password','username','phone_number']
    def save(self, **kwargs):
        user=User(
            email=self.validated_data['email']
        )
        user.set_password(self.validated_data['password'])
        user.is_student=True
        user.username=self.validated_data['username']
        user.phone_number=self.validated_data['phone_number']
        user.save()
        return user

class Adminprofileserializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = "__all__"
        extra_kwargs={
            'user':{'read_only':True},
        }

class Teacherprofileserializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        extra_kwargs={
            'user':{'read_only':True},
        }

class Studentprofileserializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        extra_kwargs={
            'user':{'read_only':True},
        }