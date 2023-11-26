from email import message
from urllib import response
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer
from rest_framework.response import  Response
from rest_framework import status
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
import io
import json
from api.twilio_API import sendMessage
import hashlib
import datetime
from datetime import date
from .forms import PasswordResetForm
from random import randint
from .serializers import UserSerializer_AllFields 
from .serializers import DriverSerializer
from .serializers import UserLocationSerializer
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt,csrf_protect
# Create your views here.



@api_view(['GET'])
def get_drivers(request):
    # Filter users who are drivers
    drivers = User.objects.filter(is_driver=True)
    serializer = UserSerializer_AllFields(drivers, many=True)  # Update the usage
    return Response(serializer.data)




def days_diff():
    now = datetime.datetime.now()
    day0 = date(2020,1,1)
    today = date(now.year,now.month,now.day)
    delta = today - day0
    return delta.days


def sixDigit_generator():
    return randint(100000,999999)


@api_view(['POST'])
def phone_number_verification(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.data
        print('data is valid')
    else:
        print('data is invalid')
        validated_data = request.data
    response = serializer.validate_entries(validated_data)
    if response != True:
        return response
    else:
        number = str(sixDigit_generator())
        phone_number = validated_data['phone_number']
        message = 'Your verification code is: ' + number
        sendMessage(phone_number,message)
        return Response(data=number,status=200)

@api_view(['POST'])
def user_save(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.data
        print('data is valid')
    else:
        print('data is invalid')
        validated_data = request.data
    response = serializer.create(validated_data)
    return response



@api_view(['POST'])      
def send_message(request):
    print(request.data)
    try:
        
        user = User.objects.get(phone_number=request.data['phone_number'])
        print("trying")
        token = str(Token.objects.get(user=user))
        username = user.username
        now = datetime.datetime.now()
        print(now.minute // 10 )
        day0 = date(2020,1,1)
        today = date(now.year,now.month,now.day)
        delta = today - day0
        delta_days = delta.days
        delta_mins = delta_days * 24 * 60 + (now.hour * 60) + now.minute    
        tens = str(delta_mins // 10)
        tens_minus_one = str(delta_mins // 10 - 1)

        #hashed_tens = hashlib.sha224(b"" + str.encode(tens)).hexdigest()
        hashed_tens_minus_one = hashlib.sha224(b"" + str.encode(tens_minus_one)).hexdigest()    
        
        
        message = ('Your Username is: '  + username +
                    '. Please click on the link below to reset your password '
                    + 'http://127.0.0.1:8000//api/password_recovery/' + token 
                    + '/' + hashed_tens_minus_one + '/'
                    )
        phone_number = request.data['phone_number']
        sendMessage(phone_number,message)
        return Response(status=200)
    except:
        return Response(data="Invalid Phone Number!",status=500)


   
def reset_password(request, token):
    user_id = Token.objects.get(key=token).user_id
    user = User.objects.get(id=user_id)
    form = PasswordResetForm()
    if request.method == 'POST':
        print(request.POST)
        data = request.POST
        if data['password1'] == data['password2']:
            user.set_password(data['password1'])
            user.save()
    context = {
        "form" : form
    }
    return render(request,"password_reset.html",context)


@api_view(['GET'])
def get_driver_details(request, driver_id):
    try:
        driver = User.objects.get(id=driver_id)
        serializer = DriverSerializer(driver)  
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)
    



class UpdateUserLocationView(View):
    @csrf_exempt  
    def post(self, request, user_id):
        # Get the user instance
        user = get_object_or_404(User, pk=user_id)

        # Create a serializer instance with the user and data from the request
        serializer = UserLocationSerializer(user, data=request.data, partial=True)

        # Validate and save the serializer
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'User location updated successfully'})
        else:
            return JsonResponse({'errors': serializer.errors}, status=400)