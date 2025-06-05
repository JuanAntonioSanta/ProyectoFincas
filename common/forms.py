from django import forms

class LoginBasicoForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={
        'placeholder': 'Introduce tu email',
        'class': 'form-control',
    }))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={
        'placeholder': 'Introduce tu contraseña',
        'class': 'form-control',
    }))
