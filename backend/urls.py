from audioop import tomono
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from api.views import user_save, get_all_stores, send_message, reset_password, phone_number_verification
import hashlib
import datetime
from datetime import date

def mins_diff():
    now = datetime.datetime.now()
    print(now.minute // 10 )
    day0 = date(2020,1,1)
    today = date(now.year,now.month,now.day)
    delta = today - day0
    delta_days = delta.days
    delta_mins = delta_days * 24 * 60 + (now.hour * 60) + now.minute
    return delta_mins

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]

urlpatterns += [
    path(r'api-token-auth/verify_creds',phone_number_verification),
    path(r'api-token-auth/create_user',user_save),
    path(r'api-token-auth/', views.obtain_auth_token),
    path(r'api/v1/get_stores/', get_all_stores),
    path(r'api/send_me_message/',send_message)
]




# user info edit endpoints for different timezones

delta_mins = mins_diff()
tens = str(delta_mins // 10)
tens_minus_one = str(delta_mins // 10 - 1)

hashed_tens = hashlib.sha224(b"" + str.encode(tens)).hexdigest()
hashed_tens_minus_one = hashlib.sha224(b"" + str.encode(tens_minus_one)).hexdigest()


urlpatterns += [
    path('api/password_recovery/<str:token>/' + hashed_tens + '/',reset_password),
    path('api/password_recovery/<str:token>/' + hashed_tens_minus_one + '/',reset_password)
]