from twilio.rest import Client
from django.conf import settings
import random
from django.contrib.auth import get_user_model


def generate_random_code():
    return random.randint(10000, 99999)

class SendOTP:
    def send_code(phone_number):
        # Generate a random 6 digit code and add it to user model 
        user = get_user_model().objects.get(phone_number=phone_number)
        user.otp = generate_random_code()
        user.save()
        # Aca deberias enviar el mensaje a traves de twillio al numero de telefono
        print(user.otp, "user otp")
        # Retorna si el usuario esta verificado o no
        return user.is_verified