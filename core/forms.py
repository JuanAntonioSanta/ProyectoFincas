from django import forms
from .models import Comunidad, Inmueble
from users.models import Usuario 

class ComunidadForm(forms.ModelForm):
    class Meta:
        model = Comunidad
        fields = ['nombre', 'direccion', 'ciudad', 'codigo_postal', 'administradores']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la comunidad'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección completa'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal'}),
            'administradores': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['administradores'].queryset = Usuario.objects.filter(tipo_usuario='ADMIN')

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['comunidad', 'identificador', 'tipo', 'propietarios']
        widgets = {
            'comunidad': forms.Select(attrs={'class': 'form-control'}),
            'identificador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1º A, Bajo B'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'propietarios': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['propietarios'].queryset = Usuario.objects.filter(tipo_usuario='CLIENTE')