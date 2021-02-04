import requests

from django import forms

from .models import MonitorObject

from config import MONITOR_TYPES, RATE_TIME


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

    def clean_url(self):
        url = self.cleaned_data.get("url")
        try:
            r = requests.get(url)
        except:
            raise forms.ValidationError("Ta strona nie działa.")

        return url

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