from accounts.utils.renderers import *
from . serializers import *
from rest_framework import generics,permissions
from rest_framework.response import Response
from accounts.models import *

class ImageUploadView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserTokenRenderer]
    serializer_class = ImageSerializers
    def post(self, request, *args, **kwargs):
        try:
            try:
                image_album = request.FILES['image_album']
            except KeyError as e:
                error_data = ResponseData.get_error_data(f"{e.args[0]} is required.")
                return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
            required_fields = ['image_album',]
            for field in required_fields:
                if not request.data.get(field):
                    error_data = ResponseData.get_error_data(f"{field} field may not be blank.")
                    return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
            except serializers.ValidationError as e:
                errors = []
                for field, error_list in e.detail.items():
                    field_error = f"{field} {error_list[0]}"
                    errors.append(field_error)
                error_data = ResponseData.custom_render(errors)
                return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(image=image_album, user=request.user)
            response_data = {
                "image":serializer.data['image'],
                "user_id":serializer.data['user'],
                "image_id":serializer.data['id'],
            }
            return Response(ResponseData.get_created_view(response_data), status=status.HTTP_201_CREATED)
        except:
            return Response(ResponseData.get_internal_server_error_data(),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ImageListView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserTokenRenderer]
    serializer_class = ImageSerializers
    def post(self, request, *args, **kwargs):
        try:
            try:
                if self.request.user.is_admin:
                    user = self.request.user
                    admin = Admin.objects.get(user=user)
                    teacher = Teacher.objects.filter(admin = admin)
                    student = Student.objects.filter(teacher__in=teacher)
                    teacherId = teacher[0].user if teacher.exists() else None
                    studentId = student[0].user if student.exists() else None
                    combined_ids = filter(None, [teacherId, studentId, user])
                    query= Images.objects.filter(user__in=combined_ids).order_by('-id')
                if self.request.user.is_teacher:
                    user = self.request.user
                    teacher = Teacher.objects.get(user = user)
                    student = Student.objects.filter(teacher=teacher)
                    studentId = student[0].user if student.exists() else None
                    combined_ids = filter(None, [studentId, user])
                    query= Images.objects.filter(user__in=combined_ids).order_by('-id')
                if self.request.user.is_student:
                    user = self.request.user
                    student = Student.objects.get(user=user)
                    query= Images.objects.filter(user=student).order_by('-id')
                if self.request.user.is_superuser:
                    query= Images.objects.all().order_by('-id')
            except Images.DoesNotExist:
                return Response(ResponseData.get_not_found_data("Image not found."), status=status.HTTP_404_NOT_FOUND)
            serializer = ImageSerializers(query, many=True)
            response_data = ResponseData.get_success_data([])
            response_data['list'] = []
            for data in serializer.data:
                response_data['list'].append({
                    "image": data["image"],
                    "user_id": data["user"],
                    "image_id": data["id"],
                })
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception:
            return Response(ResponseData.get_internal_server_error_data(), status=status.HTTP_500_INTERNAL_SERVER_ERROR)