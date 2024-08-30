from django import forms
from .models import UserProfile, Product, Cart  # Ensure Product is imported correctly
from .models import Category
from django.contrib.auth.forms import  PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import AbstractUser
from django.db import models


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'quantity', 'reorderlevel']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            # You can add widgets for other fields if needed
        }

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get('name')
    #     quantity = cleaned_data.get('quantity')
    #     price = cleaned_data.get('price')
    #     reorderlevel = cleaned_data.get('reorderlevel')

    #     if Product.objects.filter(name=name).exists():
    #         self.add_error('name', 'A product with this name already exists.')

    #     if quantity is not None and quantity < 0:
    #         self.add_error('quantity', 'Quantity cannot be negative.')

    #     if price is not None and price < 0:
    #         self.add_error('price', 'Price cannot be negative.')

    #     if reorderlevel is not None and reorderlevel < 0:
    #         self.add_error('reorderlevel', 'Reorder level cannot be negative.')

    #     return cleaned_data
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and confirm password do not match."
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'age', 'profile_picture']

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'product', 'quantity']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not UserProfile.objects.filter(email=email).exists():
            raise ValidationError("There is no user with this email address.")
        return email
# forms.py

from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import UserProfile

from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError
from .models import UserProfile

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not UserProfile.objects.filter(email=email).exists():
            raise ValidationError("There is no user with this email address.")
        return email



class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs['autocomplete'] = 'new-password'

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




from django import forms
from .models import Review

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text', 'is_from_delivered_order']

    def __init__(self, *args, **kwargs):
        super(ProductReviewForm, self).__init__(*args, **kwargs)



from django import forms
from .models import PurchaseOrder
from .models import PurchaseOrderItem
from .models import Supplier, Product



class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'username', 'password', 'email', 'address']




class OrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)



class EditProductForm(forms.Form):
    
    quantity = forms.IntegerField(label='Quantity')


from django import forms
from django.contrib.auth.forms import AuthenticationForm

class SupplierLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


from .models import PurchaseOrderstatus

class PurchaseOrderStatusForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderstatus
        fields = ['status']