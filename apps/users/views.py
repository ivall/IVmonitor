from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.contrib import messages
from django.utils.decorators import method_decorator
from apps.home.utils.tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from apps.home.utils.utils import verify_captcha, invalid_form
from apps.home.utils.EmailManager import EmailManager

from .forms import UserCreateForm, UserLoginForm
from .models import User
from .decorators import login_required


class RegisterView(CreateView):

    def get(self, request, *args, **kwargs):
        form = UserCreateForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if 'user_id' in request.session:
            messages.add_message(request, messages.ERROR, 'Jesteś już zarejestrowany.')
            return redirect('/')

        if not verify_captcha(request):
            messages.add_message(request, messages.ERROR, 'Captcha nie została uzupełniona poprawnie.')
            return redirect('/users/register')

        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.instance

            email_manager = EmailManager(user, form)
            email_manager.send_activate_email()

            messages.add_message(request, messages.SUCCESS, message='Potwierdź adres email.')
            return redirect('/users/login/')
        else:
            invalid_form(request, form)
            return redirect('/users/register/')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        if 'user_id' in request.session:
            messages.add_message(request, messages.ERROR, 'Jesteś już zalogowany.')
            return redirect('/')

        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            user = User.objects.filter(email=email, activated=True).values('id', 'username')[0]
            if not user:
                messages.add_message(request, messages.ERROR, message='Potwierdź adres email.')
                return redirect('/users/login/')

            request.session['user_id'] = user['id']
            request.session['username'] = user['username']

            messages.add_message(request, messages.SUCCESS, message='Zalogowano poprawnie.')
            return redirect('/')
        else:
            invalid_form(request, form)
            return redirect('/users/login/')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.activated = True
        user.save()
        messages.add_message(request, messages.SUCCESS, message='Adres email został potwierdzony.')
        return redirect('/users/login/')
    else:
        return HttpResponse('Link został już aktywowany lub wygasł.')


class LogoutView(View):

    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        del request.session['user_id']
        messages.add_message(request, messages.SUCCESS, message='Wylogowano poprawnie.')
        return redirect('/')

