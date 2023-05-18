from rest_framework.permissions import BasePermission

# Custom permission class to allow only admin users to perform write operations, while allowing read operations to all users


# class IsAdminOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ['GET', 'HEAD', 'OPTIONS']:
#             return True
#         return request.user.role == 'admin'


# Custom permission class to allow only teacher users to perform write operations, while allowing read operations to all users
class IsTeacherOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.role == 'teacher'


# Custom permission class to allow only parent users to perform write operations, while allowing read operations to all users
class IsParentOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.role == 'parent'


# Custom permission class to allow only student users to perform write operations, while allowing read operations to all users
class IsStudentOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.role == 'student'


# Custom permission class to allow only blogger users to perform write operations, while allowing read operations to all users
class IsBloggerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.role == 'blogger'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and their role is 'student'
        return request.user.is_authenticated and request.user.role == 'student'
    
class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and their role is 'student'
        return request.user.is_authenticated and request.user.role == 'teacher'

class IsParent(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and their role is 'student'
        return request.user.is_authenticated and request.user.role == 'parent'
