from django.shortcuts import redirect
from django.contrib import messages


def user_is_superuser(function=None, redirect_url='/'):
    """
        Decorator for views that checks that the user is NOT logged in, redirecting to the homepage if necessary by default.
    """
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            if not request.user.is_superuser:
                messages.error(request, 'You are not authorized to access this...!')
                return redirect(redirect_url)
            
            return view_func(request, *args, **kwargs)
        
        return wrapped_view
    
    if function:
        return decorator(function)
    
    return decorator