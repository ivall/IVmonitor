from django.contrib import messages
from django.shortcuts import redirect

from .models import User


def login_required():
    def decorator(function):
        def wrapper(request, *args, **kw):
            if not 'user_id' in request.session:
                messages.add_message(request, messages.ERROR, 'Nie jesteś zalogowany.')
                return redirect('/')

            user = User.objects.filter(id=request.session['user_id'], activated=True)[0]
            if not user:
                del request.session['user_id']
                messages.add_message(request, messages.ERROR, 'Nie znaleziono takiego uzytkownika lub nie aktywowałeś konta.')
                return redirect('/')

            return function(request, user, *args, **kw)
        return wrapper
    return decorator