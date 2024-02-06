from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import AdminUserCreationForm, UserAdminChangeForm
from .models import User, Admin, Teacher, Student

# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = AdminUserCreationForm
    list_display = ('email','is_superuser', 'is_admin', 'is_teacher','is_student','phone_number','username')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_admin', 'is_teacher','is_student')}),
        ('Permissions', {'fields': ('is_superuser','is_staff','is_active','groups', 'user_permissions',)}), 
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','phone_number','username')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ("groups", "user_permissions")
   
class MainAdmin(admin.ModelAdmin):
    list_display = ('token', 'user')
        
class TeacherAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_admin:
            query1 =Admin.objects.filter(user=request.user)
            query = Teacher.objects.filter(admin__in=query1)
        if request.user.is_teacher:
            query = Teacher.objects.filter(user = request.user)
        if request.user.is_superuser:
            query = Teacher.objects.all()
        return query
    list_display = ('token', 'user')

class StudentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_admin:
            query1 =Admin.objects.filter(user=request.user)
            query2 = Teacher.objects.filter(admin__in=query1)
            query = Student.objects.filter(teacher__in=query2)
        if request.user.is_teacher:
            query1 = Teacher.objects.filter(user = request.user)
            query = Student.objects.filter(teacher__in = query1)
        if request.user.is_student:
            query = Student.objects.filter(user = request.user)
        if request.user.is_superuser:
            query = Student.objects.all()
        return query
    list_display = ('token', 'user')

admin.site.register(User, UserAdmin)
admin.site.register(Admin ,MainAdmin)
admin.site.register(Teacher,TeacherAdmin)
admin.site.register(Student,StudentAdmin)