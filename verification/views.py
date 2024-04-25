from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from .forms import RegisterForm, LoginForm
from .verify import SendOTP
from django.contrib import messages
import uuid
from .check_code import CheckOTP


User = get_user_model()

def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
    "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        phone_number = form.cleaned_data.get("phone_number")
        new_user = User.objects.create_user(username, email, phone_number, password=None)
        return redirect("/login")
    return render(request, "auth/register.html", context)

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
    "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        phone_number = form.cleaned_data.get('phone_number')
        try:
            new = User.objects.get(phone_number=phone_number)
            ## if user exists
            ##first: send otp to the user    Aca enviamos el codigo a el usuario
            SendOTP.send_code(phone_number=phone_number)
            ##second:redirect to the page to enter otp 
            temp = uuid.uuid4()
            return redirect("/otp/{}/{}".format(new.pk, temp))
        except Exception as e:
            messages.error(request, "No such user exists!") 
    
    return render(request, "auth/login.html", context)

# Generar nuevos codigos OTP para el usuario. 
def generate_otp(request, pk, uuid):

    return render(request, 'otp.html' )


def check_otp(request):
    otp =request.POST.get("otp")
    phone_number = request.POST.get("phone_number")
    print('Phone number received by form ' , phone_number, 'type:', type(phone_number))
    print('otp received by form', otp, 'type', type(otp))
    otp_status= CheckOTP.check_otp(phone_number, otp) 
    if otp_status == True:
        user = authenticate(request, phone_number=phone_number) 
        print(user, "Usuario autenticado a traves de OTP")
        if user is not None:
           login(request, user, backend='verification.auth_backend.PasswordlessAuthBackend')
           return redirect("/home")
        else:
            messages.error(request, "Wrong OTP!") 

    print("otp via form: {}".format(otp))
    messages.error(request, "Wrong OTP!") 
    return render(request, "otp.html")

def home_page(request):
    return render(request, "home_page.html")
