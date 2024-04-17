from django.urls import path
from .views import *


urlpatterns = [
    path('index/', index, name='index'),
    path('category/', CategoryViewSet.as_view({'get': 'list','post':'create',})),
    path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('post/', PostViewSet.as_view({'get': 'list','post':'create',})),
    path('post/<int:pk>/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('comment/', CommentViewSet.as_view({'get': 'list','post':'create',})),
    path('comment/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),

]
