from django import forms
from .models import Usuario 


class LoginBasicoForm(forms.Form):
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu correo electrónico'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Tu contraseña'})
    )


class UsuarioCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu contraseña'})
    )
    password_confirm = forms.CharField(
        label="Confirmar Contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite tu contraseña'})
    )

    class Meta:
        model = Usuario
        fields = ('email', 'nombre', 'telefono', 'password', 'password_confirm', 'tipo_usuario') 

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu correo electrónico'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu nombre completo'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu número de teléfono (opcional)'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.tipo_usuario = 'CLIENTE'

        if commit:
            user.save()
        return user