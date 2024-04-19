from django.urls import path
from .views import *


urlpatterns = [
    path('index/', index, name='index'),
    path('category/', CategoryViewSet.as_view({'get': 'list','post':'create',}), name='category-list-create'),
    path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='category-retrieve-update-destroy'),
    path('post/', PostViewSet.as_view({'get': 'list','post':'create',}), name='post-list-create'),
    path('post/<int:pk>/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='post-retrieve-update-destroy'),
    path('comment/', CommentViewSet.as_view({'get': 'list','post':'create',}), name='comment-list-create'),
    path('comment/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='comment-retrieve-update-destroy'),

]
