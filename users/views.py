from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import user_not_authenticated
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage


# Create your views here.
def activateEmail(request, user, to_email):
    messages.success(request, f'Dear <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on \
        recieved activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')


@user_not_authenticated
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            
            return redirect('homepage')
        
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
        form = UserLoginForm(request=request, data=request.POST)
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
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                
                messages.error(request, error)

    form = UserLoginForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={"form": form}
        )
    
    
def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid:
            user_form = form.save()
            messages.success(request, f'{user_form.username}, Your profile has been updated')
            return redirect('profile', user_form.username)
        
        for error in list(form.errors.values()):
            messages.error(request, error)
    
    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(
            request=request,
            template_name='users/profile.html',
            context={'form':form}
        )
        
    else:
        return redirect('homepage')
