from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import SanPham, LoaiSanPham , Cart , Order , OrderItem
from django.http import HttpResponseRedirect
from .forms import  SuaSanPhamForm, ThemSanPhamForm, XoaSanPhamForm,ThemLoaiSanPhamForm,XoaLoaiSanPhamForm,SuaLoaiSanPhamForm,LoginForm,OrderCreateForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate , login, logout ,get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from decimal import Decimal


def index(request):
    return render(request, 'pages/home.html')

def danhSachLoaiSanPham(request):
    data = {
        'LoaiSanPham' : LoaiSanPham.objects.all()
    }
    return render(request,'pages/loaisanpham.html',data) 

def danhSachSanPham(request):
    data = {
        'SanPham' : SanPham.objects.all(),
        'LoaiSanPham' : LoaiSanPham.objects.all()
    }
    return render(request,'pages/sanpham_sell.html',data)

def danhSachSanPham_staff(request):
    data = {
        'SanPham': SanPham.objects.all()
    }
    return render(request,'pages/sanphamtable.html',data)


def chiTietSanPham(request, id):
    sanPham = SanPham.objects.get(id=id)
    data = {
        'sanPham': sanPham
    }
    return render(request, 'pages/chitietsanpham.html', data)


def themsanPham(request):
    form = ThemSanPhamForm()
    if request.method == 'POST':
        form = ThemSanPhamForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cafe/sanpham_sp')
    loaiSanPham = LoaiSanPham.objects.all()
    return render(request, 'pages/themsanpham.html', {'form': form, 'loaiSanPham': loaiSanPham})

def xoa_san_pham(request):
    if request.method == 'POST':
        form = XoaSanPhamForm(request.POST)
        if form.is_valid():
            ten_san_pham = form.cleaned_data['TenSanPham']
            try:
                san_pham = SanPham.objects.get(TenSanPham=ten_san_pham)
                san_pham.delete()
                return redirect('/cafe/sanpham_sp')
            except SanPham.DoesNotExist:
                form.add_error('TenSanPham', 'Sản phẩm không tồn tại')
    else:
        form = XoaSanPhamForm()

    return render(request, 'pages/xoasanpham.html', {'form': form})


def suasanpham(request, id):
    san_pham = get_object_or_404(SanPham, id=id)

    if request.method == 'POST':
        form = SuaSanPhamForm(request.POST, instance=san_pham)
        if form.is_valid():
            form.save()
            return redirect('/cafe/sanpham_sp')
    else:
        loaiSanPham = LoaiSanPham.objects.all()
        form = SuaSanPhamForm(instance=san_pham)
    return render(request, 'pages/suaSanpham.html', {'form': form, 'san_pham': san_pham,'loaiSanPham': loaiSanPham})

def themloaisanpham(request):
    form = ThemLoaiSanPhamForm()
    if request.method == 'POST':
        form = ThemLoaiSanPhamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/cafe/loaisanpham')
    return render(request,'pages/themloaisanpham.html',{'form': form})

def xoaloaisanpham(request):
    if request.method == 'POST':
        form = XoaLoaiSanPhamForm(request.POST)
        if form.is_valid():
            try:
                TenLoai = form.cleaned_data['TenLoai']
                loai_san_pham = LoaiSanPham.objects.get(TenLoai=TenLoai)
                if SanPham.objects.filter(LoaiSanPham=loai_san_pham).exists():
                    raise forms.ValidationError("Loại sản phẩm đang được sử dụng")
                loai_san_pham.delete()
                return redirect('/cafe/loaisanpham')
            except LoaiSanPham.DoesNotExist:
                raise forms.ValidationError("Loại sản phẩm không tồn tại")
            except Exception as e:
                error_message = str(e)
                form.add_error(None, error_message) 
    else:
        form = XoaLoaiSanPhamForm()

    return render(request, 'pages/xoaloaisanpham.html', {'form': form})

def sualoaisanpham(request, id):
    loai_sanpham = get_object_or_404(LoaiSanPham, id=id)

    if request.method == 'POST':
        form = SuaLoaiSanPhamForm(request.POST, instance= loai_sanpham)
        if form.is_valid():
            form.save()
            return redirect('/cafe/loaisanpham')
    else:
        form = SuaLoaiSanPhamForm(instance= loai_sanpham)
    return render(request, 'pages/sualoaisanpham.html', {'form': form}) 

# LOGIN VIEW
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('login')
    else:
        initial_data = {'username':'', 'password1':'','password2':""}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'pages/register.html',{'form':form})

def login_view(request): 
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            if user.is_staff : 
                return redirect ('dashboard') 
            else:  
                return redirect('/cafe/sanpham_sell') 
    else:
        initial_data = {'username':'', 'password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'pages/login.html',{'form':form}) 
  

def dashboard_view(request):
    return render(request, 'pages/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login') 
# SEARCH VIEW
def Search(request):
    if request.method == 'POST':
        searched = request.POST['searched']  
        dssp = SanPham.objects.all().filter(TenSanPham__icontains = searched)
        data = {
            'sanpham' : dssp,
            'searched': searched
        }
        return render(request, 'pages/search.html', data )
    else:
        return render(request, 'pages/search.html')

def LocSanPhamTheoLoai(request, ml):
    dssp = SanPham.objects.all().filter(LoaiSanPham=ml)
    data = {
        'LoaiSanPham' : LoaiSanPham.objects.all(),
        'LoaiSanPhamChon' : ml,
        'sanpham' : dssp,
    }
    return render(request,'pages/LocSanPhamTheoLoai.html',data)

# CART
CART_SESSION_ID = 'cart'
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(SanPham, id=product_id)
    cart.add(product,quantity=1)
    return redirect('Cart')
def cart_details(request):
    cart = Cart(request)
    products = cart.__iter__()
    total_price =0 
    for pro in products:
        total_price += pro.Gia * pro.quantity
    return render(request, 'pages/GioHang.html', {'products': products, 'total_price': total_price})
def cart_update(request, product_id, quantity):
    cart = Cart(request)
    product = get_object_or_404(SanPham, id=product_id)
    cart.update_quantity(product, quantity)
    return redirect('Cart')
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(SanPham, id=product_id)
    cart.remove(product)
    return redirect('Cart')

@login_required
def checkout(request):
    context = {}
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            my_p = request.user 
            # my_p = User.objects.get(user=request.user)
            order = form.save(commit=False)
            order.user = my_p
            order.save()
            
            total_price = 0
            cart = request.session.get('cart', {})
            print(cart)
            for product_id, product in cart:
                product_obj = SanPham.objects.get(pk=product_id)
                order_item = OrderItem.objects.create(order=order, product=product_obj, quantity=product['quantity'])
                total_price += product['quantity'] * product_obj.Gia
                order_item.save()
            order.total_price = total_price
            order.save()
        
            # del request.session[CART_SESSION_ID]
            
            return redirect('checkout_success')
        else:
            context['form'] = form
            return render(request, 'pages/home.html',context)
    else:
        form = OrderCreateForm()
        context['form'] = form
        return render(request, 'pages/GioHang.html', context)
    

 
def checkout_success(request):
    order_info = request.session.get('order_info')
    if order_info:
        order_id = order_info['order_id']
        total_price = Decimal(order_info['total_price'])
        context = {
            'order_id': order_id,
            'total_price': total_price
        }
        del request.session['order_info']  # Xóa thông tin khỏi session
        return render(request, 'pages/checkout_success.html', context)
    else:
        return redirect('home')
@login_required
def checkout_1(request):
    if request.user.is_authenticated:
        try:
            # Attempt to retrieve the user object
            user_obj = User.objects.get(id=request.user.id)
           
            order = Order.objects.create(user=user_obj, total_price=0)
            order.save()
            total_price = 0
            cart = request.session.get('cart', {})
            print(cart)
            for product_id, product in cart.items():
                product_obj = SanPham.objects.get(pk=product_id)
                order_item = OrderItem.objects.create(order=order, product=product_obj, quantity=product['quantity'])
                total_price += product['quantity'] * product_obj.Gia
                order_item.save()
            order.total_price = total_price
            order.save()
            del request.session[CART_SESSION_ID]
            request.session['order_info'] = {
             'order_id': order.id,
            'total_price': float(order.total_price)
}
            return redirect('checkout_success')
            # Now the order is created with the user assigned
        except User.DoesNotExist:
            pass
    else:
        pass
#Order
def Order_list(request):
    ds_hoadon = Order.objects.all()
    return render(request, 'pages/DSHoaDon.html', {'ds_hoadon': ds_hoadon})

def Order_item_list(request, Order_id):
    ds_cthoadon = OrderItem.objects.filter(order_id=Order_id)
    hoadon = Order.objects.get(pk = Order_id)
    context = {
        'Order': hoadon,
        'ds_cthoadon': ds_cthoadon
    }
    return render(request, 'pages/DSChiTietHoaDon.html', context)

def Delete_Order(request,Order_id):
    order = Order.objects.get(pk=Order_id)
    order.delete()
    return redirect('DSHoaDon')

def Delete_Order_item(request,Order_item_id):
    order_item = OrderItem.objects.get(pk = Order_item_id)
    price = order_item.product.Gia * order_item.quantity
    order_item.order.total_price = order_item.order.total_price - price
    order_item.order.save()
    order_id = order_item.order.id
    order_item.delete()
    return redirect('DSChiTietHD',order_id)