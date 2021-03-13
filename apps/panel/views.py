from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib import messages

from apps.users.decorators import login_required
from apps.home.utils.utils import verify_captcha, invalid_form

from .models import MonitorObject, Log, Alert
from .forms import AddMonitorForm, AddAlertForm
from config import MAX_USER_MONITORS


class PanelView(View):

    @method_decorator(login_required())
    def get(self, request, user, *args, **kwargs):
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

    @method_decorator(login_required())
    def post(self, request, user, *args, **kwargs):
        if not verify_captcha(request):
            messages.add_message(request, messages.ERROR, 'Captcha nie została uzupełniona poprawnie.')
            return redirect('/panel/')

        user_monitors = MonitorObject.objects.filter(user=user).count()
        if user_monitors >= MAX_USER_MONITORS:
            messages.add_message(request, messages.ERROR, 'Osiągnąłeś już maksymalną ilość monitorów.')
            return redirect('/panel/')

        form = AddMonitorForm(request.POST)
        if form.is_valid():
            monitor_url = form.cleaned_data['url']
            check_monitor = MonitorObject.objects.filter(user=user, url=monitor_url).exists()
            if check_monitor:
                messages.add_message(request, messages.ERROR, 'Dodałeś już taki URL.')
                return redirect('/panel/')

            form.save(user)
            messages.add_message(request, messages.SUCCESS, message='Dodano poprawnie.')
            return redirect('/panel/')
        else:
            invalid_form(request, form)


class DeleteMonitor(DeleteView):

    model = MonitorObject

    @method_decorator(login_required())
    def post(self, request, user, *args, **kwargs):
        monitor_id = request.POST.get('monitor_id')

        object = self.model.objects.filter(id=monitor_id, user=user)
        object.delete()

        messages.add_message(request, messages.SUCCESS, message='Monitor został usunięty.')
        return redirect('/panel/')


class AddAlert(CreateView):

    @method_decorator(login_required())
    def post(self, request, user, *args, **kwargs):
        form = AddAlertForm(request.POST)

        if form.is_valid():
            alerts = Alert.objects.filter(type=form.cleaned_data['type'], user_id=user.id).exists()
            if alerts:
                messages.add_message(request, messages.ERROR, 'Taki typ powiadomienia już istnieje.')
                return redirect('/panel/')

            form.save(user)
            messages.add_message(request, messages.SUCCESS, message='Dodano poprawnie.')
            return redirect('/panel/')
        else:
            invalid_form(request, form)
            return redirect('/panel/')


class DeleteAlert(DeleteView):

    model = Alert

    @method_decorator(login_required())
    def post(self, request, user, *args, **kwargs):
        alert_id = request.POST.get('alert_id')

        alert = self.model.objects.filter(id=alert_id, user=user)
        alert.delete()

        messages.add_message(request, messages.SUCCESS, message='Powiadomienie zostało usunięte.')
        return redirect('/panel/')