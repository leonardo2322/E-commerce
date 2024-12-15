from typing import Any
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView,CreateView ,DetailView
# from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView

from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import Category, Product ,Profile
from Products.utils.cart_utils import Cart_manage
from ..forms import FormCreateCategory, FormCreateProduct
from Products.utils.super_user_test import UserPassesTestMixin
from accounts.forms import CustomUserCreationForm
def vistaHome(request):
    return render(request, 'home.html')

def error_404_view(request, exception):
    return render(request, '404.html', status=404)
def error_500_view(request, exception):
    return render(request, '500.html', status=500)

def signout(request):
    logout(request)
    return redirect('login')

class SignUpView(CreateView):
    model = User
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    form_class = CustomUserCreationForm
    
    def form_valid(self, form):
        
        try:
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1']) 
            user.save()
            return redirect(self.success_url)
        except Exception as e:
            print(str(e))
        return redirect(self.success_url)
       

    def form_invalid(self, form):
        return render(self.request, self.template_name, {
            'form': form,
            'error_message': 'Por favor corrige los errores en el formulario.',
            'status': 'error'
        })

class login_View(LoginView):
    template_name = "registration/login.html"
    
    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.request.user
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)

        cart = Cart_manage(self.request)
        cart.sync_with_user(user)
        return response
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class CategoryListView(LoginRequiredMixin,UserPassesTestMixin,ListView):
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
        
    def test_func(self):
        return self.request.user.is_superuser

    
class CreatItemCategory(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Category
    form_class = FormCreateCategory
    template_name = 'Categoryes/createItemCategory.html'
    success_url = reverse_lazy("category_list")
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Categoria'
        return context
    def test_func(self):
        return self.request.user.is_superuser


class CreateItemProduct(LoginRequiredMixin,UserPassesTestMixin,CreateView):
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
    
    def test_func(self):
        return self.request.user.is_superuser
    
class ListViewProduct(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Product
    template_name = 'products/listProduct.html'
    context_object_name = 'products'
    success_url = reverse_lazy("list_Product")
  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'listado de Productos'
        context['urls'] = reverse_lazy("create_product")
        return context
    
    def test_func(self):
        return self.request.user.is_superuser


    
    
class ViewProducts(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'products/CardsProducts.html'
    paginate_by = 9
    ordering = ['-created']
    
    def get_queryset(self):
        busqueda = self.request.GET.get('search', '')
        filtro = self.request.GET.get('filter','')
        if busqueda:
            queryset = Product.objects.filter(name__icontains=busqueda)
            return queryset
        if filtro:
            if filtro == 'todos':
                queryset = Product.objects.all()
                return queryset
            categoria_obj  = get_object_or_404(Category, name=filtro)
            queryset = Product.objects.filter(cate=categoria_obj)
            return queryset
        queryset = Product.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categoryes"] = Category.objects.all()
        return context
    
    