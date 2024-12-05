from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from validate_email import validate_email
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from tracker.decorators import user_should_not_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from utils import generate_token



def send_activate_email(request, user):
    current_site = get_current_site
    email_subject = "Activate your account"
    email_body = render_to_string("authentication/activate",{
        "user": user,
        "domain": current_site,
        "uid":urlsafe_base64_decode(force_bytes(user.pk)),
        "token": generate_token.make_token(user)
    })
 


def register(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        context = {"has_error" : False, "data":request.POST}


        if not validate_email(email):
            messages.add_message(request, messages.ERROR, "Correct Email is required")
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR, "Username required")
            context['has_error'] = True

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, "Password must be more than 6 characters")
            context['has_error'] = True

        if password!=password2:
            messages.add_message(request, messages.ERROR, "Password not matched")
            context["has_error"] = True
        
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "Username is taken already")
            context["has_error"] = True
        
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, "email is taken, choose another one")
            context["has_error"] = True
        
        
        if context["has_error"] == False:
    
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()

            send_activate_email(request, user)

            messages.add_message(request, messages.ERROR, "Account created successfully")
            login(request, user)
            messages.add_message(request, messages.SUCCESS, f"Welcome {user.username}")
            return redirect(reverse('home'))
     
    return render(request, 'authentication/register.html')



@user_should_not_access
def login_user(request):
    if request.method == "POST":
        context = {"data":request.POST}
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if not user.is_email_verified:
            messages.add_message(request, messages.ERROR, "Activate your account Please, check inbox and spam for email")
            return render(request, 'authentication/login.html',context)
        
        if not user:
            messages.add_message(request, messages.ERROR, "Invalid username or password considering signing up")
            return render(request, 'authentication/login.html',context)

        login(request, user)
        messages.add_message(request, messages.SUCCESS, f"Welcome {user.username}")
        return redirect(reverse('home'))

    return render(request, 'authentication/login.html')



def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, f"{{request.user.username}} Logout successful")
    return redirect(reverse('login'))

