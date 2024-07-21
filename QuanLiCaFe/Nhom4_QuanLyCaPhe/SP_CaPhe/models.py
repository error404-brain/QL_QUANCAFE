from django.db import models 
from django.contrib.auth.models import User

# Create your models here.
class LoaiSanPham(models.Model):
    TenLoai = models.CharField(max_length = 100)
    

class SanPham(models.Model):
    TenSanPham = models.CharField(max_length=100)
    Gia = models.DecimalField(max_digits=10, decimal_places=2)
    MoTa = models.TextField()
    Anh = models.CharField(max_length=255)
    LoaiSanPham = models.ForeignKey(LoaiSanPham, on_delete=models.CASCADE)
    Suger_level = models.CharField(max_length=50, default='unknown')
    Topping_checkbox = models.CharField(max_length=50, default='unknown')

# CART
CART_SESSION_ID = 'cart'
class Cart:
    def __init__(self,request) :
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
    def __iter__(self):
        product_ids = self.cart.keys()
        products = SanPham.objects.filter(id__in=product_ids)
        for product in products:
            product.quantity = self.cart[str(product.id)]['quantity']
        return products
    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        print(self.cart[product_id]['quantity'])
        self.cart[product_id]['quantity'] += quantity
        self.save()
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def update_quantity(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            if quantity == 0:
                del self.cart[product_id]
            else:
                self.cart[product_id]['quantity'] = quantity
            self.save()
    def save(self):
        self.session.modified = True
    def total_price(self):
        total = 0
        for product in self.cart.values():
            total += product['quantity'] * product['price']  # Giả sử mỗi sản phẩm có trường price
        return total
    def clear(self):
        del self.session[CART_SESSION_ID]
        self.session.modified = True
# giỏ hàng
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
# chi tiết giỏ hàng
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(SanPham, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
   