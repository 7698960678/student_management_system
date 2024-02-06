from django.contrib import admin
from .models import Images
from accounts.models import *

# Register your models here.
class ImageAlbum(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(email=request.user.email)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_queryset(self, request):
        if request.user.is_admin:
            user = request.user
            admin = Admin.objects.get(user=user)
            teacher = Teacher.objects.filter(admin = admin)
            student = Student.objects.filter(teacher__in=teacher)
            teacherId = teacher[0].user if teacher.exists() else None
            studentId = student[0].user if student.exists() else None
            combined_ids = filter(None, [teacherId, studentId, user])
            query= Images.objects.filter(user__in=combined_ids).order_by('-id')
        if request.user.is_teacher:
            user = request.user
            teacher = Teacher.objects.get(user = user)
            student = Student.objects.filter(teacher=teacher)
            studentId = student[0].user if student.exists() else None
            combined_ids = filter(None, [studentId, user])
            query= Images.objects.filter(user__in=combined_ids).order_by('-id')
        if request.user.is_student:
            user = request.user
            student = Student.objects.get(user=user)
            query= Images.objects.filter(user=student).order_by('-id')
        if request.user.is_superuser:
            query= Images.objects.all().order_by('-id')
        return query
    list_display = ('id','image', 'user')
admin.site.register(Images,ImageAlbum)
