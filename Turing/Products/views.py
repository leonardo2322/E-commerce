from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView,CreateView
from django.views import View
# from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Category, Product
from .forms import FormCreateCategory, FormCreateProduct
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db import IntegrityError

def vistaHome(request):
    return render(request, 'home.html')
def signout(request):
    logout(request)
    return redirect('login')
class SignUpView(CreateView):
    model = User
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    form_class = UserCreationForm
    
    def form_valid(self, form):
        try:
            # Guardar el usuario
            user = form.cleaned_data['username']
            print(form.cleaned_data)
            if User.objects.filter(username=user).exists():
                return render(self.request, 'registration/signup.html', {'error_message': 'Error al crear el usuario.'})
            else:
                if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                    
                    user = form.save(commit=False)
                    user.set_password(form.cleaned_data['password1'])
                    user.save()
                    return redirect(self.success_url)
        except IntegrityError:
            return render(self.request, 'registration/signup.html', {'error_message': 'Error al crear el usuario.'})

    def form_invalid(self, form):
        # Si el formulario es inválido, renderizar el formulario nuevamente con los errores
       
        return render(self.request, self.template_name, {'form': form})


class login_View(LoginView):
    template_name = "registration/login.html"
    

class CategoryListView(ListView):
    model = Category
    template_name = 'Categoryes/listCategory.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        print(request)
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'listado_de_tareas'
        context['urls'] = reverse_lazy("create_category")
        return context
class CreatItemCategory(CreateView):
    model = Category
    form_class = FormCreateCategory
    template_name = 'Categoryes/createItemCategory.html'
    success_url = reverse_lazy("category_list")
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Categoria'
        return context
    
class CreateItemProduct(CreateView):
    model = Product
    form_class = FormCreateProduct
    template_name = 'products/createProduct.html'
    def post(self, request, *args, **kwargs):
        data = {}
        try:
         action = request.POST['action']
         if action == 'add':
             form = self.get_form()
             if form.is_valid():
                 form.save()
                 data['success'] = 'se han ingresado los datos'
             else:
                 data = form.errors
         else:
             data['error'] = 'Ha ocurrido un error al insertar los datos'
        except Exception as e:
            print(e)
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Item Product'
        context['action'] = 'add'
        return context
    
class ListViewProduct(ListView):
    model = Product
    template_name = 'products/listProduct.html'
    success_url = reverse_lazy("list_Product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'listado de Productos'
        context['urls'] = reverse_lazy("create_product")
        return context
    


class ViewProducts(ListView):
    model = Product
    template_name = 'products/CardsProducts.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)