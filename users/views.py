from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from .models import Usuario
from .forms import UsuarioCreationForm, LoginBasicoForm #UsuarioChangeForm 
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Vistas para el modelo Usuario
class UsuarioListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'users/usuario_list.html'
    context_object_name = 'usuarios'
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_administrador

    def get_queryset(self):
        return Usuario.objects.all().order_by('nombre')


class UsuarioDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Usuario
    template_name = 'users/usuario_detail.html'
    context_object_name = 'usuario'
    permission_required = 'users.view_usuario'

class UsuarioCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioCreationForm # Usamos nuestro formulario de creación personalizado
    template_name = 'users/usuario_form.html'
    success_url = reverse_lazy('usuario_list') # Redirecciona a la lista de usuarios
    permission_required = 'users.add_usuario'

class UsuarioUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = 'users/usuario_form.html'
    context_object_name = 'usuario'
    success_url = reverse_lazy('usuario_list')
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_administrador

class UsuarioDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'users/usuario_confirm_delete.html'
    context_object_name = 'usuario'
    success_url = reverse_lazy('usuario_list')
    permission_required = 'users.delete_usuario'


class UsuarioRegistrationView(CreateView):
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = 'proyecto/register.html' # La plantilla HTML del formulario de registro


    
    success_url = reverse_lazy('home') 

    def form_valid(self, form):
        user = form.save() 
        
        if user is not None:
            login(self.request, user)
        
        return super().form_valid(form)


# View para el inicio de sesión básico

def login_basico(request):
    error = None
    form = LoginBasicoForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Cambia esto según tu vista principal
            else:
                error = "Credenciales incorrectas"
        else:
            # Si el formulario no es válido (ej. campos vacíos)
            error = "Por favor, introduce tu email y contraseña."


    return render(request, 'proyecto/login.html', {'form': form, 'error': error})