from django.urls import path
from . import views 

urlpatterns = [
    path('', views.login_view, name='login'),
    # Sản Phẩm (Khánh Hưng)
    path('index', views.index, name='index'),
    path('loaisanpham', views.danhSachLoaiSanPham, name='danhSachLoaiSanPham'),
    path('sanpham_sell',views.danhSachSanPham, name='danhSachSanPham'),
    path('sanpham_sp', views.danhSachSanPham_staff, name ='danhSachSanPham_staff'),
    path('chitietsanpham/<int:id>/', views.chiTietSanPham, name='chitietsanpham'),
    path('themsanpham',views.themsanPham,name='themsanpham'),
    path('xoasanpham',views.xoa_san_pham, name='xoa_san_pham'),
    path('suasanpham/<int:id>/',views.suasanpham,name='suasanpham'),
    path('themloaisanpham',views.themloaisanpham,name='themloaisanpham'),
    path('xoaloaisanpham',views.xoaloaisanpham,name='xoaloaisanpham'),
    path('sualoaisanpham/<int:id>/',views.sualoaisanpham,name='sualoaisanpham'), 
    # login_path (Tấn Phát)
    path('login/',views.login_view,name='login') ,   
    path('logout/',views.logout_view,name='logout') ,
    path('register/',views.register_view,name='register'), 
    path('dashboard/',views.dashboard_view,name='dashboard'),
    #Search_path (Thu Thủy)
    path('LocSanPhamTheoLoai/<int:ml>', views.LocSanPhamTheoLoai, name='LocSanPhamTheoLoai'),
    path('search', views.Search, name='Search'),
    #Cart (Minh Khoa)
    path('Cart',views.cart_details,name='Cart'),
    path('add_to_cart/<int:product_id>/',views.cart_add,name='add_to_cart'),
    path('update_quantity/<int:product_id>/<int:quantity>/', views.cart_update, name='update_cart'),
    path('delete_cart/<int:product_id>',views.cart_remove,name='delete_cart'),
    path("checkout", views.checkout_1, name="checkout"),
    path('checkout-success/', views.checkout_success, name='checkout_success'),
    #Order (Minh Khoa)
    path('Order',views.Order_list,name='DSHoaDon'),
    path('Order_Item/<int:Order_id>',views.Order_item_list,name='DSChiTietHD'),
    path('Order_Delete/<int:Order_id>',views.Delete_Order,name='XoaHD'),
    path('Order_item_delete/<int:Order_item_id>',views.Delete_Order_item,name='XoaCTHD')

]
