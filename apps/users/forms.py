from django import forms

from .models import User
from .utils import hash_password, verify_password


class UserCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Nazwa użytkownika"
        self.fields['password_confirm'].widget.attrs['onchange'] = 'onChange()'
        self.fields['password'].widget.attrs['onchange'] = 'onChange()'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    password = forms.CharField(label='Hasło', widget=forms.PasswordInput, max_length=32)
    password_confirm = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput, max_length=32)

    class Meta:
        model = User
        fields = ('username', 'email', 'password_confirm', 'password')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username=username).exists()
        if user:
            raise forms.ValidationError("Użytkownik z takim loginem już istnieje.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email=email).exists()
        if user:
            raise forms.ValidationError("Użytkownik z takim emailem już istnieje.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Hasła nie zgadzają się.")

        password = hash_password(password).decode('utf-8')
        return password

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserLoginForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    password = forms.CharField(label='Hasło', widget=forms.PasswordInput, max_length=32)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        user = User.objects.filter(email=email).exists()
        if not user:
            raise forms.ValidationError("Użytkownik z takim emailem nie istnieje.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")

        user = User.objects.filter(email=email).values('password')

        if not verify_password(password, user[0]['password']):
            raise forms.ValidationError('Niepoprawne hasło.')

        return password