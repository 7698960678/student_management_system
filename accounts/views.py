from rest_framework import generics,permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsAdmin,IsSuperuser,IsTeacher
from .serializers import *
from django.contrib.auth import authenticate
from accounts.utils.renderers import *
from rest_framework_simplejwt.tokens import RefreshToken

#### Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

### Login View
class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data, context={'request':request})
        try:
            if serializer.is_valid(raise_exception=True):
                email=serializer.data.get('email')
                password = serializer.data.get('password')
                user = authenticate(email=email, password=password)
                if user is not None:
                    access_refresh_token=get_tokens_for_user(user) 
                    token, created=Token.objects.get_or_create(user=user)
                    response_data = {
                        'key':token.key,
                        'id':user.pk,
                        'email': user.email,
                        'is_superuser' :  user.is_superuser,
                        'is_admin':user.is_admin,
                        'is_teacher':user.is_teacher,
                        'is_student':user.is_student,
                    }
                    return Response(ResponseData.get_success_login_view(access_refresh_token['access'], access_refresh_token['refresh'],response_data),status=status.HTTP_200_OK)
                else:
                    return Response(ResponseData.get_error_data("Email or Password is not Valid"), status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            for field, error_list in e.detail.items():
                errors = []
                field_error = f"{field} {error_list[0]}"
                errors.append(field_error)
            error_data = ResponseData.custom_render(errors)
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_data = ResponseData.get_error_data(str(e))
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

class AdminSignupView(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated&IsSuperuser]
    serializer_class = AdminSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user=serializer.save()
                access_refresh_token=get_tokens_for_user(user)
                response_data = ResponseData.get_created_data({
                    "key":Token.objects.get(user=user).key,
                    'id': user.pk,
                    'email': user.email,
                    'is_admin':user.is_admin,
                    'is_teacher':user.is_teacher,
                    'is_student':user.is_student,
                    "accessToken": access_refresh_token['access'],
                    "refreshToken": access_refresh_token['refresh']
                    })
                return Response(response_data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            for field, error_list in e.detail.items():
                errors = []
                field_error = f"{field} {error_list[0]}"
                errors.append(field_error)
            error_data = ResponseData.custom_render(errors)
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

class TeacherSignupView(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated&IsAdmin]
    renderer_classes = [UserRenderer]
    serializer_class = TeacherSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user=serializer.save()
                token = Token.objects.get(user=user)
                accesstoken = get_tokens_for_user(user)
                admin = Admin.objects.get(user= self.request.user)
                Teacher.objects.create(user=user,token = token,admin = admin)
                response_data = ResponseData.get_created_data({
                    "user":UserSerializer(user, context=self.get_serializer_context()).data,
                    "token":Token.objects.get(user=user).key,
                    "accessToken" : accesstoken,
                    "message":"account created successfully"
                })
                return Response(response_data,status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            for field, error_list in e.detail.items():
                errors = []
                field_error = f"{field} {error_list[0]}"
                errors.append(field_error)
            error_data = ResponseData.custom_render(errors)
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

class StudentSignupView(generics.GenericAPIView):
    permission_classes=[permissions.IsAuthenticated&IsTeacher]
    renderer_classes = [UserRenderer]
    serializer_class = StudentSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                user=serializer.save()
                token = Token.objects.get(user=user)
                accesstoken = get_tokens_for_user(user)
                teacher = Teacher.objects.get(user =self.request.user)
                Student.objects.create(user=user,token = token,teacher = teacher)
                response_data = ResponseData.get_created_data({
                    "user":UserSerializer(user, context=self.get_serializer_context()).data,
                    "token":Token.objects.get(user=user).key,
                    "accessToken" : accesstoken,
                    "message":"account created successfully"
                })
                return Response(response_data,status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            for field, error_list in e.detail.items():
                errors = []
                field_error = f"{field} {error_list[0]}"
                errors.append(field_error)
            error_data = ResponseData.custom_render(errors)
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
