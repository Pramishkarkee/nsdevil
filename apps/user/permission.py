from rest_framework.permissions import BasePermission


class IsTeacherUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and user.user_type=="teacher_user")

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)

class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and user.user_type=="student")

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)