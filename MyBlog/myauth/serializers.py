from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=50)
    last_name = serializers.CharField(required=True, max_length=50)
    username = serializers.CharField(required=True,max_length=50)
    password = serializers.CharField(
        write_only=True,
        required=True,
        max_length=50,
    )

    
    def validate(self, attrs):
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError("This username already exists!")
        return attrs
    
    def create(self, validated_data):
        User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return self.validated_data

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['first_name','last_name','username']

