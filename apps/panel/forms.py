import requests

from django import forms

from .models import MonitorObject, Alert

from config import MONITOR_TYPES, RATE_TIME, ALERT_TYPES


class AddMonitorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddMonitorForm, self).__init__(*args, **kwargs)
        self.fields['rate'].widget.attrs['class'] = 'form-range'

        for field in self.fields:
            if field != 'rate':
                self.fields[field].widget.attrs['class'] = 'form-control'

    rate = forms.IntegerField(widget=forms.NumberInput(attrs={'type':'range', 'min':'1', 'max':'60', 'value': '30'}))

    class Meta:
        model = MonitorObject
        fields = ('name', 'rate', 'type', 'url')

    def clean_type(self):
        type = self.cleaned_data.get("type")
        if type not in MONITOR_TYPES:
            raise forms.ValidationError("Niepoprawny typ monitora.")

        return type

    def clean_rate(self):
        rate = self.cleaned_data.get("rate")
        rate = int(rate)

        if rate not in RATE_TIME:
            raise forms.ValidationError("Niepoprawny czas sprawdzania.")

        return rate

    def save(self, user):
        name = self.cleaned_data.get("name")
        rate = self.cleaned_data.get("rate")
        type = self.cleaned_data.get("type")
        url = self.cleaned_data.get("url")

        monitor = MonitorObject(
            name=name,
            rate=rate,
            type=type,
            url=url,
            user=user
        )

        monitor.save()
        return monitor


class AddAlertForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddAlertForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'rate':
                self.fields[field].widget.attrs['class'] = 'form-control'

    post_value = forms.CharField(widget=forms.Textarea, required=False)
    url = forms.URLField(required=False)

    class Meta:
        model = Alert
        fields = ('name', 'type', 'url', 'post_value')

    def clean_type(self):
        type = self.cleaned_data.get("type")
        if type not in ALERT_TYPES:
            raise forms.ValidationError("Niepoprawny typ powiadomienia.")

        print(type)
        if type == 'webhook':
            post_value = self.data.get("post_value")
            url = self.data.get("url")

            if not post_value or not url:
                raise forms.ValidationError("Uzupełnij dane potrzebne do webhooka.")

        return type

    def save(self, user):
        type = self.cleaned_data.get("type")
        name = self.cleaned_data.get("name")
        post_value = self.cleaned_data.get("post_value")
        url = self.cleaned_data.get("url")

        alert = Alert(
            name=name,
            post_value=post_value,
            type=type,
            url=url,
            user=user
        )

        alert.save()
        return alert