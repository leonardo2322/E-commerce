from django.urls import path
from .views import *
from django.conf.urls import handler404, handler500

handler404 = 'Products.views.error_404_view'
handler500 = 'Products.views.error_500_view'
urlpatterns = [
    path('', vistaHome ,name='home'),
    path("list/categories", CategoryListView.as_view(), name='category_list'),
    path("create/category", CreatItemCategory.as_view(), name="create_category"),
    path('create/product', CreateItemProduct.as_view(), name="create_product"),
    path('list/product', ListViewProduct.as_view(), name='list_Product'),
    path('login/', login_View.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name="signup" ),
    path('accounts/logout/', signout, name="logout"),
    path('products/', ViewProducts.as_view(), name='products')
]
