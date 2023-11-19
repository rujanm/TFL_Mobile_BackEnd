from email import message
from urllib import response
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .serializers import StoreSerializer, UserSerializer
from rest_framework.response import  Response
from rest_framework import status
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
import io
from api.models import Store
import json
from api.twilio_API import sendMessage
import hashlib
import datetime
from datetime import date
from .forms import PasswordResetForm
from random import randint
# Create your views here.




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


@api_view(['GET'])
def get_all_stores(request):
    serializer = StoreSerializer(data=Store.objects.all(), many=True)
    serializer.is_valid()
    data = json.dumps(serializer.data)
    data = json.loads(data)
    
    return Response(data=data, status=200)

@api_view(['POST'])      
def send_message(request):
    print(request.data)
    try:
        user = User.objects.get(phone_number=request.data['phone_number'])
        token = str(Token.objects.get(user=user))
        username = user.username
        delta_days = days_diff()
        delta_hours = delta_days * 24
        delta_minutes = delta_hours * 60
        tens = str(delta_minutes // 10)
        hashed_tens = hashlib.sha224(b"" + str.encode(tens)).hexdigest()
        
        message = ('Your Username is: '  + username +
                    '. Please click on the link below to reset your password '
                    + 'http://10.0.2.2:8000/api/password_recovery/' + token 
                    + '/' + hashed_tens + '/'
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