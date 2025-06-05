from django.contrib import admin
from .models import Comunidad, Inmueble

# Register your models here.
class ComunidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'ciudad', 'codigo_postal', 'get_administradores')
    search_fields = ('nombre', 'direccion', 'ciudad', 'administradores__nombre')
    list_filter = ('ciudad', 'administradores')
    ordering = ('nombre',)
    list_per_page = 10
    list_editable = ('direccion', 'ciudad', 'codigo_postal')

    def get_administradores(self, obj):
        return ", ".join([str(a.nombre) for a in obj.administradores.all()])
    get_administradores.short_description = 'Administradores'

class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('comunidad', 'identificador', 'tipo', 'get_propietarios')
    search_fields = ('comunidad__nombre', 'identificador', 'tipo', 'propietarios__nombre')
    list_filter = ('comunidad', 'tipo')
    ordering = ('comunidad',)
    list_per_page = 10
    list_editable = ('identificador', 'tipo')

    def get_propietarios(self, obj):
        return ", ".join([str(p.nombre) for p in obj.propietarios.all()])
    get_propietarios.short_description = 'Propietarios'

admin.site.register(Comunidad, ComunidadAdmin)
admin.site.register(Inmueble, InmuebleAdmin)