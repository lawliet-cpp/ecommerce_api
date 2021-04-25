from rest_framework import serializers
from .models import *
from django.core import exceptions
from django.contrib.auth import authenticate
import django.contrib.auth.password_validation as validators
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=155)
    password = serializers.CharField(max_length=50)



    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User.objects.create_user(email=email,password=password)
        return user

    def validate(self,validated_data):
        password = validated_data.get("password")
        err = dict()
        try:
            validators.validate_password(password)
        except exceptions.ValidationError as e:
            err["password"] = e

        if err:
            raise serializers.ValidationError(err)

        return super(UserSerializer,self).validate(validated_data)







class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
 

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=155)
    password = serializers.CharField(max_length=155)
    def validate(self,validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = authenticate(email=email,password=password)
        if user is not None:
            validated_data["user"] = user
            return validated_data
        else:
            raise serializers.ValidationError("Cannot login with the provided credentials")

        