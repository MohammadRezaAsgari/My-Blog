from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer

class UserCreateView(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):   
        register_serializer = RegisterSerializer(data=request.data)
        if register_serializer.is_valid():
            
            register_serializer.create(register_serializer.validated_data)
            return Response(register_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)