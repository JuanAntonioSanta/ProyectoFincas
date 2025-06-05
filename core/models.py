from django.db import models
from users.models import Usuario

# Create your models here.

class Comunidad(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=5)
    administradores = models.ManyToManyField(
        Usuario,
        related_name='comunidades_llevadas', # Nombre inverso para acceder desde Usuario
        blank=True,
        limit_choices_to={'tipo_usuario': 'ADMIN'} # Opcional: Solo permite seleccionar usuarios de tipo 'ADMIN'
    )

    class Meta:
        verbose_name_plural = "Comunidades"

    def __str__(self):
        return self.nombre


class Inmueble(models.Model):
    comunidad = models.ForeignKey(Comunidad, related_name='inmuebles', on_delete=models.CASCADE)
    identificador = models.CharField(max_length=100)  # Por ejemplo: "1º A", "Bajo B"
    tipo = models.CharField(max_length=50, choices=[
        ('vivienda', 'Vivienda'),
        ('local', 'Local'),
        ('garaje', 'Garaje'),
        ('trastero', 'Trastero'), 
        ('plaza', 'Plaza de garaje'),
    ])
    propietarios = models.ManyToManyField(
            Usuario,
            related_name='inmuebles_propietario', # Nombre inverso para acceder desde Usuario
            blank=True,
            limit_choices_to={'tipo_usuario': 'CLIENTE'} # Opcional: Solo permite seleccionar usuarios de tipo 'CLIENTE'
        )

    def __str__(self):
        return f"{self.identificador} - {self.comunidad.nombre}"
