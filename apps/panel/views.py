import json

from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib import messages

from apps.users.decorators import login_required
from apps.home.utils import verify_captcha
from apps.users.models import User

from .models import MonitorObject, Log, Alert
from .forms import AddMonitorForm, AddAlertForm
from config import MAX_USER_MONITORS


class PanelView(View):
    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.session['user_id'])
        monitors = MonitorObject.objects.filter(user=user)
        alerts = Alert.objects.filter(user=user)
        logs = Log.objects.filter(monitor_object__user_id=user.id).order_by('-id')[:10]
        context = {
            'addMonitorForm': AddMonitorForm(),
            'addAlertForm': AddAlertForm(),
            'monitors': monitors,
            'alerts': alerts,
            'logs': logs
        }
        return render(request, 'panel/panel.html', context=context)


class AddMonitor(CreateView):

    queryset = MonitorObject.objects.all()

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        if not verify_captcha(request):
            messages.add_message(request, messages.ERROR, 'Captcha nie została uzupełniona poprawnie.')
            return redirect('/panel/')

        user = User.objects.get(id=request.session['user_id'])
        user_monitors = MonitorObject.objects.filter(user=user).count()
        if user_monitors == MAX_USER_MONITORS:
            messages.add_message(request, messages.ERROR, 'Osiągnąłeś już maksymalną ilość monitorów.')
            return redirect('/panel/')

        form = AddMonitorForm(request.POST)
        if form.is_valid():
            form.save(user)
            messages.add_message(request, messages.SUCCESS, message='Dodano poprawnie.')
            return redirect('/panel/')
        else:
            errors = json.loads(form.errors.as_json())
            for error in errors:
                messages.add_message(request, messages.ERROR, message=errors[error][0]['message'])

            return redirect('/panel/')


class DeleteMonitor(DeleteView):

    model = MonitorObject

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        monitor_id = request.POST.get('monitor_id')

        user = User.objects.get(id=request.session['user_id'])
        object = MonitorObject.objects.filter(id=monitor_id, user=user)
        object.delete()

        messages.add_message(request, messages.SUCCESS, message='Monitor został usunięty.')
        return redirect('/panel/')


class AddAlert(CreateView):

    queryset = Alert.objects.all()

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        form = AddAlertForm(request.POST)

        if form.is_valid():
            user = User.objects.get(id=request.session['user_id'])
            alerts = Alert.objects.filter(type=form.cleaned_data['type'], user_id=user.id).exists()
            if alerts:
                messages.add_message(request, messages.ERROR, 'Taki typ powiadomienia już istnieje.')
                return redirect('/panel/')
            form.save(user)
            messages.add_message(request, messages.SUCCESS, message='Dodano poprawnie.')
            return redirect('/panel/')
        else:
            errors = json.loads(form.errors.as_json())
            print(errors)
            for error in errors:
                messages.add_message(request, messages.ERROR, message=errors[error][0]['message'])

            return redirect('/panel/')


class DeleteAlert(DeleteView):

    model = Alert

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        alert_id = request.POST.get('alert_id')

        user = User.objects.get(id=request.session['user_id'])
        object = Alert.objects.filter(id=alert_id, user=user)
        object.delete()

        messages.add_message(request, messages.SUCCESS, message='Powiadomienie zostało usunięte.')
        return redirect('/panel/')