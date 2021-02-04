import json
import threading

from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib import messages

from apps.users.decorators import login_required
from apps.home.utils import verify_captcha
from apps.users.models import User

from .models import MonitorObject
from .forms import AddMonitorForm


from .checker import get_sites
t1 = threading.Thread(target=get_sites)
t1.start()


class PanelView(View):
    @method_decorator(login_required())
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.session['user_id'])
        monitors = MonitorObject.objects.filter(user=user)
        context = {
            'addMonitorForm': AddMonitorForm(),
            'monitors': monitors
        }
        return render(request, 'panel/panel.html', context=context)


class AddMonitor(CreateView):

    queryset = MonitorObject.objects.all()

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        if not verify_captcha(request):
            messages.add_message(request, messages.ERROR, 'Captcha nie została uzupełniona poprawnie.')
            return redirect('/panel/')

        form = AddMonitorForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.session['user_id'])
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