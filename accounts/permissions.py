from rest_framework.permissions import BasePermission
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from accounts.utils.renderers import *

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and request.user.is_admin):
            raise PermissionDenied("You do not have permission to perform this action.")
        return True
    def process_permission_denied(self, exc):
        return Response(exc, status=status.HTTP_400_BAD_REQUEST)

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if not(request.user.is_authenticated and request.user.is_teacher):
            raise PermissionDenied("You do not have permission to perform this action.")
        return True
    def process_permission_denied(self, exc):
        return Response(exc, status=status.HTTP_400_BAD_REQUEST)

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if not(request.user.is_authenticated and request.user.is_student):
            raise PermissionDenied("You do not have permission to perform this action.")
        return True
    def process_permission_denied(self, exc):
        return Response(exc, status=status.HTTP_400_BAD_REQUEST)

## IsSuperuser
class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        if not(request.user.is_authenticated and request.user.is_superuser):
            raise PermissionDenied("You do not have permission to perform this action.")
        return True
    def process_permission_denied(self, exc):
        return Response(exc, status=status.HTTP_400_BAD_REQUEST)