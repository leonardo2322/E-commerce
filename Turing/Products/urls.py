from django.urls import path
from .views import *

urlpatterns = [
    path('', vistaHome ,name='home'),
    path("list/categories", CategoryListView.as_view(), name='category_list'),
    path("create/category", CreatItemCategory.as_view(), name="create_category"),
    path('create/product', CreateItemProduct.as_view(), name="create_product"),
    path('list/product', ListViewProduct.as_view(), name='list_Product'),
    path('login/', login_View.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name="signup" ),
    path('accounts/profile/',vistaHome,name="profile"),
    path('accountslogout/', signout, name="logout"),
    path('products/', ViewProducts.as_view(), name='products')
]
