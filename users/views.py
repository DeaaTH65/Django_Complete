from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .decorators import user_not_authenticated


# Create your views here.
@user_not_authenticated
def register(request):    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"New account registered {user.username}")
            return redirect('/')
        
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
                
    else:
        form = UserRegistrationForm()
        
    return render(
        request=request,
        template_name='users/register.html',
        context={'form': form}
    )
    
    
@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("homepage")


@user_not_authenticated
def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("homepage")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error) 

    form = AuthenticationForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={"form": form}
        )