from django import forms
from .models import SanPham , LoaiSanPham , Order
from django.contrib.auth.forms import AuthenticationForm

class ThemSanPhamForm(forms.ModelForm):
    class Meta:
        model = SanPham
        fields = ['TenSanPham', 'Gia', 'MoTa', 'Anh', 'LoaiSanPham', 'Suger_level','Topping_checkbox']

    def clean_TenSanPham(self):
        TenSanPham = self.cleaned_data['TenSanPham']

        try:
            SanPham.objects.get(TenSanPham=TenSanPham)
        except SanPham.DoesNotExist:
            return TenSanPham
        raise forms.ValidationError("Sản phẩm đã tồn tại")

    def save(self):
        san_pham = SanPham(
            TenSanPham=self.cleaned_data['TenSanPham'],
            Gia=self.cleaned_data['Gia'],
            MoTa=self.cleaned_data['MoTa'],
            Anh=self.cleaned_data['Anh'],
            LoaiSanPham=self.cleaned_data['LoaiSanPham'],
            Suger_level=self.cleaned_data['Suger_level'],
            Topping_checkbox = self.cleaned_data['Topping_checkbox']
        )
        san_pham.save()


class XoaSanPhamForm(forms.Form):
    TenSanPham = forms.CharField(max_length=100)

    def clean_TenSanPham(self):
        TenSanPham = self.cleaned_data['TenSanPham']
        try:
            san_pham = SanPham.objects.get(TenSanPham=TenSanPham)
        except SanPham.DoesNotExist:
            raise forms.ValidationError("Sản phẩm không tồn tại")
        return TenSanPham

class SuaSanPhamForm(forms.ModelForm):
    class Meta:
        model = SanPham
        fields = ['TenSanPham', 'Gia', 'MoTa', 'Anh', 'LoaiSanPham', 'Suger_level','Topping_checkbox']

    def clean_TenSanPham(self):
        TenSanPham = self.cleaned_data['TenSanPham']
        return TenSanPham

    def save(self, commit=True):
        san_pham = super().save(commit=False)
        san_pham.Suger_level = self.cleaned_data['Suger_level']
        san_pham.Topping_checkbox = self.cleaned_data['Topping_checkbox']
        if commit:
            san_pham.save()
        return san_pham
    
class ThemLoaiSanPhamForm(forms.ModelForm):
    TenLoai = forms.CharField(label='Tên thể loại', max_length=100)

    class Meta:
        model = LoaiSanPham
        fields = ['TenLoai']

    def clean_TenLoai(self):
        ten_loai = self.cleaned_data['TenLoai']
        try:
            LoaiSanPham.objects.get(TenLoai=ten_loai)
        except LoaiSanPham.DoesNotExist:
            return ten_loai
        raise forms.ValidationError("Thể loại đã tồn tại")

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    
class XoaLoaiSanPhamForm(forms.Form):
    TenLoai = forms.CharField(max_length=100)
    def clean_TenLoai(self):
        TenLoai = self.cleaned_data['TenLoai']
        try:
            loai_san_pham = LoaiSanPham.objects.get(TenLoai=TenLoai)
            if SanPham.objects.filter(LoaiSanPham=loai_san_pham).exists():
                raise forms.ValidationError("Loại sản phẩm đang được sử dụng")
        except LoaiSanPham.DoesNotExist:
            raise forms.ValidationError("Loại sản phẩm không tồn tại")
        return TenLoai
    
class SuaLoaiSanPhamForm(forms.ModelForm):
    class Meta:
        model = LoaiSanPham
        fields = ['TenLoai']

    def clean_TenLoai(self):
        TenLoai = self.cleaned_data['TenLoai']
        return TenLoai

    def save(self, commit=True):
        loai_sanpham = self.instance
        loai_sanpham.TenLoai = self.cleaned_data['TenLoai']

        if commit:
             loai_sanpham.save()
        return  loai_sanpham
    
class LoginForm (AuthenticationForm): 
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


# Order form
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('total_price',)