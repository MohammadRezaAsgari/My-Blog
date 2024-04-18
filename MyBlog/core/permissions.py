from rest_framework.permissions import BasePermission
from .models import Post, Comment


class IsOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj.author == request.user