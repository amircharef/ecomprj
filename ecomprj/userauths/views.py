from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import User   

# User = settings.AUTH_USER_MODEL


def register_view(request) :

    if request.method == "POST" : 
        form = UserRegisterForm(request.POST or None)        
        if form.is_valid() : 
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Your account was created successfully.")
            new_user = authenticate(username=form.cleaned_data.get("email"),
                                    password=form.cleaned_data.get("password1"))
            login(request, new_user)
            return redirect("core:index")
    else : 
        form = UserRegisterForm()        
        
    context = {
        'form': form,
    }
    return render(request, "userauths/sign-up.html", context)

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Hey, you are already logged in.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in.")
            return redirect("core:index")
        else:
            messages.warning(request, "Invalid email or password, or create an account.")

    return render(request, "userauths/sign-in.html")

def logout_view(request) : 
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")
