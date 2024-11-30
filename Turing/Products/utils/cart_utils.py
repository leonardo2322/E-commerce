from Products.models import Cart ,Product, Cart_Item, Profile
class Cart_manage:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        
        cart = self.session.get("cart")
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart


    def add(self, product,cant=None):

        if str(product.id) not in self.cart.keys():
            self.cart[str(product.id)] = {
                'id': int(product.id),
                'name' : product.name,
                'cant': cant if cant  is not None else 1,
                'price':float(product.pvp),
                'image':product.image.url
            }
            print(self.cart,"---------en cart")
        else:
            for key, value in self.cart.items():
                if key == str(product.id):
                    value['cant'] = value['cant'] + 1
                    
                    break
        self.save()
    def save(self):
        print("----------------guardando")
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def decrement(self, product):
        for key, value in self.cart.items():
                if key == str(product.id):
                    value['cant'] = value['cant'] - 1
                    if value['cant'] < 1:
                        self.remove(product)
                    else:
                        self.save()
                    break

                else:
                    print("no existe el producto")


    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

    def sync_with_user(self,user):
        """
        Sincroniza el carrito de la sesión con el carrito en la base de datos.
        """
        if not user.is_authenticated:
            return
        
        # Obtener o crear el carrito en la base de datos
        cart, created = Cart.objects.get_or_create(client=user)

        # Fusionar los datos de la sesión con la base de datos
        for product_id , item in self.cart.items():
            product = Product.objects.get(id=item['id'])
            cart_item, created = Cart_Item.objects.get_or_create(cart=cart,prods=product)
            cart_item.cant = max(cart_item.cant,item['cant'])
            cart_item.save()


        self.clear()

    def load_from_db(self,user):
        """
        Carga el carrito desde la base de datos a la sesión.
        """
         
        if not self.request.user.is_authenticated:
            return
        
        try:
            cart = Cart.objects.get(client=user)
            for item in cart.items.all():
                self.cart[str(item.product.id)] = {
                    'id': item.product.id,
                    'name': item.product.name,
                    'cant': item.cant,
                    'price': float(item.product.pvp),
                    'image': item.product.image.url
                }
            self.save()
        except Cart.DoesNotExist:
            print("------------carrito no existente")
            pass