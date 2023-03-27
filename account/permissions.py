from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'

class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'parent'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'

class IsBlogger(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'blogger'
