from django.urls import path, include
from . import views

urlpatterns = [
    path('admin_login/', views.combined_login, name='combined_login'),
    path('search/', views.search, name='search'),
    path('login/', views.combined_login, name='user_login'),
    path('user_login/', views.combined_login, name='combined_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('admin_add/', views.admin_add, name='admin_add'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('adminpageorder/', views.admin_order_view, name='adminorders'),
    path('adminordersiteam/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('userpageorder/', views.user_order_view, name='orders'),
    path('', views.index, name='index'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_to_wishlist/<int:product_id>/', views.remove_to_wishlist, name='remove_to_wishlist'),
    path('decrease/<int:product_id>/', views.decrease_to_cart, name='decrease_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/decrease/<int:product_id>/', views.decrease_to_cart, name='decrease_quantity'),

    
    path('cart/', views.cart, name='cart'),
    path('view_to_wishlist/', views.view_to_wishlist, name='view_to_wishlist'),
    path('checkout/', views.checkout_view, name='checkout'),  
    path('order_summary/', views.order_summary_view, name='order_summary'),  
    path('profile/update/', views.profile_update, name='profile_update'),
    path('update_status/<int:order_id>/', views.update_status, name='update_status'),
    path('order_list_and_detail/', views.order_list_and_detail, name='order_list_and_detail'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('refund_order/<int:order_id>/', views.refund_order, name='refund_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('admin/orders/', views.admin_order_view, name='admin_order_view'),
    path('create_category/', views.create_category, name='create_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('product/<int:product_id>/add_review/', views.add_product_review, name='add_product_review'),
    
    path('purchase_orders/', views.purchase_orders, name='purchase_orders_list'),

    # Password reset URLs
    path('reset_password/', views.auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_done/', views.auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', views.auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Supplier-related URLs
    path('register/supplier/', views.register_supplier, name='register_supplier'),
    path('suppliers_list/', views.suppliers_list, name='suppliers_list'),
    path('edit_supplier/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),
    path('delete_supplier/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),
    path('supplier/purchase-orders/', views.supplier_purchase_orders, name='supplier_purchase_orders'),
    path('send_purchase_order_email/<int:order_id>/', views.send_purchase_order_email, name='send_purchase_order_email'),
    path('reorder/<int:product_id>/', views.reorder_product, name='reorder_product'),
    
    # New Supplier Dashboard URLs
    
    #path('supplier/orders/', views.supplier_orders, name='supplier_orders'),
    # path('supplier/account/', views.supplier_account, name='supplier_account'),
    path('supplier/login/', views.supplier_login, name='supplier_login'),
    path('supplier/dashboard/', views.supplier_dashboard, name='supplier_dashboard'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),  
    
    
    path('admin-page/purchase_orders/', views.admin_purchase_orders, name='admin_purchase_orders'),
    path('admin-page/update_stock/<int:order_id>/', views.admin_update_stock, name='admin_update_stock'),
    path('admin-page/update_delivered_quantity/<int:order_id>/', views.update_delivered_quantity, name='update_delivered_quantity'),
    path('view_invoice/<int:order_id>/', views.view_invoice, name='view_invoice'),
    path('view_supplier_invoice/<int:order_id>/', views.view_supplier_invoice, name='view_supplier_invoice'),
    
]



