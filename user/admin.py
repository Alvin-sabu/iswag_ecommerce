from django.contrib import admin 
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import PurchaseOrderItem




# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(PurchaseOrderItem)
admin.site.register(PurchaseOrder)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['fullname', 'address', 'postal_code']


from .models import Supplier

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'username', 'email', 'address']
    search_fields = ['company_name', 'username', 'email']
    readonly_fields = ['password']  # Don't allow editing password in admin

admin.site.register(Supplier, SupplierAdmin)

