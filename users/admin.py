from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('nombre', 'email', 'telefono', 'tipo_usuario', 'is_active')
    list_filter = ('tipo_usuario', 'is_active')
    search_fields = ('email', 'nombre')
    ordering = ('nombre',)

    # Definición de los fieldsets para la página de detalle/edición de un usuario
    fieldsets = (
        (None, {'fields': ('email', 'password')}), # Información básica de autenticación
        ('Información Personal', {'fields': ('nombre', 'telefono')}), # Campos personalizados
        ('Permisos y Roles', {'fields': ('is_active', 'is_superuser', 'tipo_usuario')}), # Permisos y el nuevo campo de tipo de usuario
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}), # Campos de AbstractBaseUser
        ('Relaciones', {'fields': ('inmuebles_propiedad', 'comunidades_administradas')}), # Nuevas relaciones ManyToMany
    )

    # Campos para añadir un nuevo usuario (solo para create_user)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2', 'nombre', 'telefono', 'tipo_usuario'),
        }),
    )

