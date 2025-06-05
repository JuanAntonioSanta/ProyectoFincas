from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Comunidad, Inmueble
from .forms import ComunidadForm, InmuebleForm

# Vistas para la Comunidad
class ComunidadListView(LoginRequiredMixin, ListView):
    model = Comunidad
    template_name = 'proyecto/comunidad_list.html'
    context_object_name = 'comunidades'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.is_administrador:
            return queryset
        elif self.request.user.is_authenticated and self.request.user.tipo_usuario == 'CLIENTE':
            comunidad_ids_del_cliente = Inmueble.objects.filter(
                propietarios=self.request.user
            ).values_list('comunidad__id', flat=True).distinct()
            return queryset.filter(id__in=comunidad_ids_del_cliente)
        return Comunidad.objects.none()

class ComunidadDetailView(LoginRequiredMixin, DetailView):
    model = Comunidad
    template_name = 'proyecto/comunidad_detail.html'
    context_object_name = 'comunidad'
    login_url = reverse_lazy('login')


class ComunidadCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Comunidad
    form_class = ComunidadForm
    template_name = 'proyecto/comunidad_form.html'
    success_url = reverse_lazy('comunidad_list')
    login_url = reverse_lazy('login')
                                
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_administrador

    raise_exception = False

    def form_valid(self, form):
        comunidad = form.save(commit=False)
        comunidad.save() 
        if self.request.user.is_administrador:
            comunidad.administradores.add(self.request.user)
        return super().form_valid(form)

class ComunidadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comunidad
    form_class = ComunidadForm
    template_name = 'proyecto/comunidad_form.html'
    context_object_name = 'comunidad'
    success_url = reverse_lazy('comunidad_list')
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_administrador

class ComunidadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comunidad
    template_name = 'proyecto/comunidad_confirm_delete.html'
    success_url = reverse_lazy('comunidad_list')
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_administrador

# Vistas para el Inmueble
class InmuebleListView(LoginRequiredMixin, ListView):
    model = Inmueble
    template_name = 'proyecto/inmueble_list.html'
    context_object_name = 'inmuebles'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_administrador:
            return Inmueble.objects.all()
        elif self.request.user.is_authenticated and self.request.user.tipo_usuario == 'CLIENTE':
            return Inmueble.objects.filter(propietarios=self.request.user)
        return Inmueble.objects.none() 

class InmuebleDetailView(LoginRequiredMixin, DetailView):
    model = Inmueble
    template_name = 'proyecto/inmueble_detail.html'
    context_object_name = 'inmueble'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.tipo_usuario == 'CLIENTE':
            return queryset.filter(propietarios=self.request.user)
        return queryset

class InmuebleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = 'proyecto/inmueble_form.html'
    success_url = reverse_lazy('inmueble_list')
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_administrador


class InmuebleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = 'proyecto/inmueble_form.html'
    context_object_name = 'inmueble'
    success_url = reverse_lazy('inmueble_list')
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_administrador


class InmuebleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Inmueble
    template_name = 'proyecto/inmueble_confirm_delete.html'
    success_url = reverse_lazy('inmueble_list')
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_administrador