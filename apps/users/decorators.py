from django.contrib import messages
from django.shortcuts import redirect

from .models import User


def login_required():
    def decorator(function):
        def wrapper(request, *args, **kw):
            if not 'user_id' in request.session:
                messages.add_message(request, messages.ERROR, 'Nie jesteś zalogowany.')
                return redirect('/')

            user = User.objects.filter(id=request.session['user_id'], activated=True).exists()
            if not user:
                del request.session['user_id']
                messages.add_message(request, messages.ERROR, 'Potwierdź adres email.')
                return redirect('/')

            return function(request, *args, **kw)
        return wrapper
    return decorator