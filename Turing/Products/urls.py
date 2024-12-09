from django.urls import path
from django.conf.urls import handler404, handler500, handler403

from .views.views_principal import *
from .views.views_sale import Show_product_view ,Model_List_View ,Add_cart_view,Remove_item_cart,Sale_items_cart,List_hystory_purchase
from .views.views_del_and_put import Category_Delete_View, Category_update_view,Product_delete_view,Product_update_view
handler404 = 'Products.views.error_404_view'
handler500 = 'Products.views.error_500_view'

def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)
handler403 = custom_403_view
urlpatterns = [
    path('', vistaHome ,name='home'),
    path("list/categories", CategoryListView.as_view(), name='category_list'),
    path("create/category", CreatItemCategory.as_view(), name='create_category'),
    path('update/category/<int:pk>/', Category_update_view.as_view(), name='update_category'),
    path('delete/category/<int:pk>/', Category_Delete_View.as_view(), name='delete_category'),

    path('create/product', CreateItemProduct.as_view(), name='create_product'),
    path('list/product', ListViewProduct.as_view(), name='list_Product'),
    path('delete/product/<int:pk>/', Product_delete_view.as_view(), name='delete_product'),
    path('update/product/<int:pk>/', Product_update_view.as_view(), name='update_product'),


    path('login/', login_View.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup' ),
    path('accounts/logout/', signout, name='logout'),
    path('products/', ViewProducts.as_view(), name='products'),
    path('product/<int:pk>/', Show_product_view.as_view(), name='show_product' ),
    path('cart/', Model_List_View.as_view(), name='cart'),
    path('add_to_cart/',Add_cart_view.as_view(), name='add_cart' ),
    path('eliminar/<int:pk>/', Remove_item_cart.as_view(),name="Eliminar_Cart"),
    path('comprar/',Sale_items_cart.as_view(), name='comprar' ),
    path('historial/',List_hystory_purchase.as_view(), name='history' )
]
