from pyexpat import model
from .models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import phonenumbers
from rest_framework.response import  Response

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                "first_name",
                "last_name" ,
                "email" ,
                "phone_number",
                "password",
                "username"
                     ]

    def validate_entries(self, validated_data):
        user = User(email=validated_data['email'],
            username=validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            phone_number = validated_data['phone_number'],
        )
        print('line25')
        # If email already exists
        if validated_data['email'] != '':
            if User.objects.filter(email=validated_data['email']).exists():
                print('email not unique')
                return Response(data="Email Already Exists!", status=500)
        # if Phone number field is empty        
        if validated_data['phone_number'] == '':
            return Response(data="Please Enter a Valid Phone Number!                       (e.g., +12345678900)", status=500)
        # checks if phone number is valid or not
        try:
            phone_number = phonenumbers.parse(validated_data['phone_number'], None)
            if phonenumbers.is_valid_number(phone_number):
                pass
            else:
                return Response(data="Please Enter a Valid Phone Number!                         (e.g., +12345678900)", status=500)
        except:
            return Response(data="Please Enter a Valid Phone Number!                        (e.g., +12345678900)", status=500)
        # checks if the phone number exists
        if User.objects.filter(phone_number=validated_data['phone_number']).exists():
                return Response(data="Phone Number Already Exists!", status=500)
        if User.objects.filter(username=validated_data['username']).exists():
            return Response(data="This Username Already Exists!", status=500)
        return True

    def create(self, validated_data):
        user = User(email=validated_data['email'],
            username=validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            phone_number = validated_data['phone_number'],
            phone_verified  = True
        )
        user.set_password(validated_data['password'])
        user.save()
        return Response(data="User created successfully", status=200)



class UserSerializer_AllFields(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'latitude', 'longitude', 'is_driver']
        
        
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'latitude', 'longitude']
        
        
class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['longitude', 'latitude']