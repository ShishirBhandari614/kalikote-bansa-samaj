from django.shortcuts import redirect
from functools import wraps

def superadmin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'superadmin':
            return view_func(request, *args, **kwargs)
        return redirect('no_permission')  # Or login page
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in ['subadmin', 'superadmin']:
            # Subadmin and superadmin can access
            return view_func(request, *args, **kwargs)
        return redirect('no_permission')
    return wrapper
