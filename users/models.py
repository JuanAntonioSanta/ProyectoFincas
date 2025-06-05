from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db) 
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('tipo_usuario', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

# Modelo base de usuario
class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPO_USUARIO_CHOICES = (
        ('CLIENTE', 'Cliente'),
        ('ADMIN', 'Administrador'),
    )

    # Necesario para Django Allauth
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='CLIENTE')

    # --- CAMPOS ESENCIALES PARA DJANGO ADMIN ---
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre'] 

    def __str__(self):
        return self.nombre

    @property
    def is_cliente(self):
        return self.tipo_usuario == 'CLIENTE'
    
    @property
    def is_administrador(self):
        return self.tipo_usuario == 'ADMIN'
    
    def save(self, *args, **kwargs):
        if not self.username and self.email:
            self.username = self.email.split('@')[0] + str(self.pk or '')
            # Mejor: user.username = get_random_string(length=10) o similar para asegurar unicidad
        super().save(*args, **kwargs)