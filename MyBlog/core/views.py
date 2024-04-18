from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Category, Post, Comment
from .serializers import *
from .filters import PostFilter
from .permissions import IsOwner

SAFE_METHODS = ('GET', 'HEAD' , 'OPTIONS')
NOT_SAFE_METHODS = ('POST','PUT','PATCH','DELETE')
EDIT_METHODS = ('PUT','PATCH','DELETE')

def index(request):
    return

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer 
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = PostFilter

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny(), ]
        elif self.request.method in NOT_SAFE_METHODS:
            return [IsAuthenticated(),]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer 

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny(), ]
        elif self.request.method in NOT_SAFE_METHODS:
            if self.request.method in EDIT_METHODS:
                return [IsOwner(),]
            return [IsAuthenticated(),]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super().perform_create(serializer)
