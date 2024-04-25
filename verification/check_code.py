import os
from twilio.rest import Client
from django.conf import settings
from django.contrib.auth import get_user_model


class CheckOTP:
    
    def check_otp(phone_number, otp_code):
        user = get_user_model().objects.get(phone_number=phone_number)
        if user.otp == otp_code:
            user.is_verified = True
            user.is_active = True
            user.save()
            return user.is_verified
        print('user otp', user.otp, 'otp received by form', otp_code)
        print('user verified? ', user.is_verified)
        return user.is_verified