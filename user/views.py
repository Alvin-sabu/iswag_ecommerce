from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import EditProductForm, OrderForm, ProductForm, PurchaseOrderStatusForm
from .models import Product, Review
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.shortcuts import render, redirect
from .models import Order
from .forms import UserProfileForm
from django.db.models import F
from django.http import HttpResponseBadRequest
from .models import Category
from .forms import CategoryForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from .forms import ProductReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import SupplierForm  # Assuming you have a SupplierForm defined
from .forms import SupplierLoginForm 
from .forms import PurchaseOrderstatus







def adminpage(request):
    products_at_reorder_level = Product.objects.filter(quantity__lte=F('reorderlevel'))
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'products_at_reorder_level': products_at_reorder_level,
        'productdata': products,
        'categories': categories,
    }
    
    return render(request, 'user.html', context)

from .forms import SupplierLoginForm  # Import the SupplierLoginForm

def combined_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    # Redirect superuser to admin page
                    return redirect('adminpage')
                
                
                else:
                    # Redirect regular user to index page
                    return redirect('index')
        else:
            error_message = 'Invalid credentials. Please try again.'
            return render(request, 'user_login.html', {'form': form, 'error_message': error_message})
    
    else:
        form = AuthenticationForm()

    return render(request, 'user_login.html', {'form': form})

# def admin_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None and user.is_superuser:
#                 login(request, user)
#                 url='/adminpage'
#                 x=f'''
#                     <script>
#                         alert("welcome admin");
#                         window.location.href = "{url}"; 
#                     </script>
#                 '''
                
#                 return HttpResponse(x)
#         else:
#             form = AuthenticationForm()  
#             error_message = 'Invalid credentials. Please try again.'
#             return render(request, 'admin_login.html', {'form': form, 'error_message': error_message})
    
#     else:
#         form = AuthenticationForm()

#     return render(request, 'admin_login.html', {'form': form})


from django.contrib.auth import login, get_backends, get_user_model
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def user_register(request):
    registration_successful = False

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Customize saving email if needed
            user.email = form.cleaned_data['email']
            user.save()

            # Find the backend path
            from django.conf import settings
            backend = settings.AUTHENTICATION_BACKENDS[0]

            # Login with the backend
            login(request, user, backend=backend)
            registration_successful = True
            return redirect('user_login')  # Adjust URL name as needed
    else:
        form = CustomUserCreationForm()

    return render(request, 'user_register.html', {'form': form, 'registration_successful': registration_successful})


# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'user_login.html', {'form': form})


def user_logout(request):
    logout(request)
    # Redirect to the index page after logout

    return redirect('index')


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages

import logging
from django.shortcuts import redirect
from django.contrib import messages

logger = logging.getLogger(__name__)

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            user = form.save(commit=False)
            password = password_form.cleaned_data['new_password1']
            if password:
                user.set_password(password)  # Use set_password method to update password
            user.save()
            password_form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_login')  # Redirect to the user_login page after successful update
    else:
        form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'profile_update.html', {'form': form, 'password_form': password_form})
from .forms import ProductForm  # Assuming you have a ProductForm defined

def admin_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the form data
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image = form.cleaned_data['image']
            quantity = form.cleaned_data['quantity']
            reorderlevel = form.cleaned_data['reorderlevel']
            category_name = form.cleaned_data['category']  # Get category name from the form

            # Check if any field is negative
            if quantity >= 0 and price >= 0 and reorderlevel >= 0:
                # Create a new product instance
                new_product = form.save(commit=False)  # Create the product instance without saving to database yet
                new_product.category = category_name  # Assign category name to the product
                new_product.save()  # Save the new product to the database
                return redirect('adminpage')  # Redirect after adding a product
            else:
                # Return a bad request response indicating invalid data
                return HttpResponseBadRequest("Invalid data. Quantity, price, and reorder level cannot be negative.")
    else:
        form = ProductForm()

    return render(request, 'admin_add.html', {'form': form})

def create_category(request):
    message = ''  # Initialize the message variable

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Category added!'  # Set success message
            return redirect('adminpage')
        else:
            message = 'Error adding category!'  # Set error message
    else:
        form = CategoryForm()

    context = {
        'form': form,
        'message': message,  # Pass the message to the template
    }
    
    # Return a response with the message instead of rendering the template directly
    return HttpResponse(pop_message(request, 'create_category.html', context))

def delete_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('adminpage')
    return render(request, 'delete_category.html', {'category': category})

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    category_filter = request.GET.get('category')
    if category_filter:
        # Filter products based on the category name field in the Product model
        products = Product.objects.filter(category__iexact=category_filter)

    context = {
        'productdata': products,
        'categories': categories,
        'selected_category': category_filter,
    }
    return render(request, 'index.html', context)

from django.urls import reverse



def product_list(request): #admin page product view
    products = Product.objects.all()
    return render(request, 'user/user.html', {'product': products})


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from .models import Product, Category
from .forms import ProductForm

def edit_product(request, product_id):
    product_to_edit = get_object_or_404(Product, pk=product_id)
    print(product_to_edit.category)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_to_edit)
        if form.is_valid():
            # new_quantity = form.cleaned_data['quantity']
            # new_price = form.cleaned_data['price']
            # new_reorder_level = form.cleaned_data['reorderlevel']
            # if new_quantity >= 0 and new_price >= 0 and new_reorder_level >= 0:
            form.save()
            print('ok')
            return redirect('adminpage')  # Redirect to the user page
        else:
            return HttpResponseBadRequest("Invalid data. Quantity, price, and reorder level cannot be negative.")
    else:
        # Initialize the form with the instance
        form = ProductForm(instance=product_to_edit, initial={'category': product_to_edit.category})
        # Select the correct category for the product being edited
        form.fields['category'].queryset = Category.objects.all()

    # Render the template with the form
    return render(request, 'edit_product.html', {'form': form, 'product': product_to_edit})


def delete_product(request, product_id):
    product_to_delete = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        confirmation = request.POST.get('confirmation', None)
        if confirmation == 'confirmed':
            product_to_delete.delete()  # Delete the product from the database
            return redirect('adminpage')  # Redirect to the admin page after deletion
        else:
            return redirect('adminpage')  # Redirect without deleting if not confirmed

    return render(request, 'confirmation_page.html', {'product': product_to_delete})

def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(name__icontains=query, is_active=True)
    return render(request, 'search_results.html', {'products': products, 'query': query})

def search_view(request):
    query = request.GET.get('query', '')  # Get the 'query' parameter from the request's GET parameters

    if query:
        # Perform a search using the query, ensuring it's not None
        products = Product.objects.filter(name__icontains=query)
    else:
        # Handle the case where 'query' is None or empty
        products = []

    context = {
        'query': query,
        'products': products,
    }

    return render(request, 'search_results.html', context)

from requests import request




from django.core.mail import send_mail

def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = 0
    for item in cart_items:
        total_amount += item.quantity * item.product.price

    if request.method == 'POST':
        # Retrieve form data
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        payment_method = request.POST.get('payment_method')

        if payment_method == 'cash_on_delivery':
            # Process Cash on Delivery order - no additional steps required
            pass

        elif payment_method == 'card':
            card_number = request.POST.get('card_number')
            # Process Card payment - simulated for demo

        elif payment_method == 'upi':
            upi_id = request.POST.get('upi_id')
            # Process UPI payment - simulated for demo

        elif payment_method == 'net_banking':
            bank_name = request.POST.get('bank_name')
            # Process Net Banking payment - simulated for demo

        # Create the order and order items
        order = Order.objects.create(
            user=request.user,
            fullname=fullname,
            address=address,
            city=city,
            postal_code=postal_code,
            total_amount=total_amount,
        )

        # Retrieve and add cart items to the order
        for cart_item in cart_items:
            order.items.create(product=cart_item.product, quantity=cart_item.quantity)
        
        # Clear cart items for the current user after order creation
        cart_items.delete()

        # Construct redirect URL with parameters
        redirect_url = reverse('order_summary')
        params = {
            'fullname': fullname,
            'address': address,
            'city': city,
            'postal_code': postal_code,
            'total_amount': total_amount,
            'cart_products': order.items.all(),  # Pass order items to order summary view
        }

        redirect_url += '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
       # Send email confirmation to the logged-in user's email address
        subject = 'Order Confirmation - iWATCH'
        message = f"Dear {fullname},\n\n"
        message += f"Thanks for ordering with iWATCH.\n\n"
        message += f"For order details, click the following link:\n"
        message += f"Or Please click TRACK ORDER button in your iWATCH account "
        message += "Best regards,\niWATCH Team"

        sender_email = 'alvinksabu200115@email.com'  # Replace with your sender email
        recipient_email = request.user.email  # Use the logged-in user's email address
        send_mail(subject, message, sender_email, [recipient_email], html_message=message)

        # Redirect to order summary page
        return HttpResponseRedirect(redirect_url)

    return render(request, 'checkout.html', {'total_amount': total_amount})



import ast
from django.http import HttpResponseServerError
import re

def order_summary_view(request):
    fullname = request.GET.get('fullname')
    address = request.GET.get('address')
    city = request.GET.get('city')
    postal_code = request.GET.get('postal_code')
    total_amount = request.GET.get('total_amount')
    cart_products = request.GET.get('cart_products')

    print("Cart Products:", cart_products)  # Debug print to check cart_products value

    # Define a regular expression pattern to extract product name and quantity
    pattern = r"<OrderItem: (\d+) x (.+?) in order \d+>"
    cart_items_dict = {}

    # Extract product details from the cart_products string using regular expressions
    matches = re.findall(pattern, cart_products)
    print("Matches:", matches)  # Debug print to check extracted matches

    if matches:
        for match in matches:
            quantity = int(match[0])
            product_name = match[1]
            # Check if the product_name already exists in the dictionary
            if product_name in cart_items_dict:
                cart_items_dict[product_name] += quantity
            else:
                cart_items_dict[product_name] = quantity
    else:
        return HttpResponseServerError("No cart items found.")

    # Convert the dictionary to a list of dictionaries for template rendering
    cart_items = [{'product_name': name, 'quantity': qty} for name, qty in cart_items_dict.items()]

    context = {
        'fullname': fullname,
        'address': address,
        'city': city,
        'postal_code': postal_code,
        'total_amount': total_amount,
        'cart_products': cart_items,
    }

    return render(request, 'order_summary.html', context)
from .models import Cart
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required(login_url=combined_login)
def add_to_cart(request, product_id):

    product = Product.objects.get(pk=product_id)
    # print(isinstance(request.user,UserProfile)
    if request.method=='POST':
        if product.quantity > 0:
            cart_item = Cart(user=request.user, product=product, quantity=1)  # Adjust quantity as needed
            cart_item.save()
            # Decrease product quantity by 1
            product.quantity -= 1
            product.save()
            # Redirect to the cart page or product detail page
            return redirect('cart')  # Redirect to cart page or wherever you manage cart items
        else:
            # Handle out of stock case
            return render(request, 'out_of_stock.html', {'product': product})

def decrease_to_cart(request, product_id):
    # Get the cart item corresponding to the product and the current user
    cart_item = Cart.objects.filter(product_id=product_id, user=request.user).first()

    if cart_item is not None:
        if cart_item.quantity > 1:  # Check if quantity is greater than 1 to avoid negative quantity
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # Reduce product quantity and delete cart item if quantity is 1
            product = get_object_or_404(Product, pk=product_id)
            product.quantity += 1  # Add the item back to product stock
            product.save()
            cart_item.delete()  # Remove the item from cart

    return redirect('cart')

from django.db.models import Sum
def remove_from_cart(request, product_id):
    # Filter cart items by product and user
    cart_items = Cart.objects.filter(product_id=product_id, user=request.user)

    # Get the product associated with the cart items
    product = get_object_or_404(Product, pk=product_id)

    # Aggregate to get the total quantity of items in the cart for this product
    total_quantity = cart_items.aggregate(total_quantity=Sum('quantity'))['total_quantity']

    if total_quantity:
        # Increase the product quantity by the total quantity of items being removed
        product.quantity += total_quantity
        product.save()

    # Delete all cart items for the user and product
    cart_items.delete()

    return redirect('cart')



from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, Product

@login_required
def cart(request):
    upcart_items = Cart.objects.filter(user=request.user)
    
    
    # <QuerySet [<Cart: Cart for alvin: Apple VX max>, <Cart: Cart for alvin: Apple VX max>]>
    cart_items={}
    for item in upcart_items:
        # print(item.product.name)
        
        if item.product.name in cart_items:
            cart_items[item.product.name]['quantity']+=1
            cart_items[item.product.name]['total_price']+=cart_items[item.product.name]['price']
            
        else:
            cart_items[item.product.name]={
                'id':item.product.id,
                'name':item.product.name,
                'price':item.product.price,
                'quantity':item.quantity,
                'price':item.product.price,
                'total_price':item.product.price,
                'image':item.product.image
            }
            # print(cart_items)

    total_price = sum(item['total_price'] for item in cart_items.values())

    
    context= {
        'cart_items': cart_items,
        'total_price': total_price
        }
    
    return render(request, 'cart.html',context)
 
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    has_delivered_order = False
    reviews = []  # Default value

    if user.is_authenticated:
        orders = Order.objects.filter(user=user, status='delivered', items__product=product)
        if orders.exists():
            has_delivered_order = True
        reviews = Review.objects.filter(product=product)

    # Create a form instance and pass it to the context
    form = ProductReviewForm()
    context = {
        'product': product,
        'user': user,
        'has_delivered_order': has_delivered_order,
        'reviews': reviews,
        'form': form,  # Add the form to the context
    }

    return render(request, 'product_detail.html', context)

 
@login_required(login_url=combined_login)
def add_to_wishlist(request, product_id):
    if 'wishlist' not in request.session:  
        request.session['wishlist'] = []  

    wishlist = request.session['wishlist'] 
    if product_id not in wishlist:  
        wishlist.append(product_id)
        request.session['wishlist'] = wishlist 
        message='Item added to your wishlist!'
    else:
        message='Item already in wishlist'

    url='/'
    return HttpResponse(pop_message(url,message))
#return HttpRespone
    
@login_required(login_url=combined_login)
def remove_to_wishlist(request, product_id):
    wishlist = request.session['wishlist']   
    wishlist.remove(product_id)
    request.session['wishlist']=wishlist
    return redirect('index')





@login_required(login_url=combined_login)
def view_to_wishlist(request):
    if 'wishlist' not in request.session:  
        context={
            'product':'',
        }
    else:
        wishlist = request.session['wishlist'] 
        data=Product.objects.filter(id__in=wishlist)
        
        context={
            'data':data
        }

    return render(request,'wishlist.html',context)



#custom popup message

def pop_message(url,message):
    url=url
    x=f'''
        <script>
            alert("{message}");
            window.location.href = "{url}"; 
        </script>
    '''
    return(x)



@login_required
def admin_order_view(request):
    # Admin view to display all orders
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'order_list_and_detail.html', context)

@login_required
def order_detail_view(request, order_id):
    # Admin view to display order details
    order = Order.objects.get(id=order_id)
    items = order.items.all()
    context = {'order': order, 'items': items}
    return render(request, 'order_detail.html', context)

@login_required
def update_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        try:
            order = Order.objects.get(pk=order_id)
            if order.status != 'cancelled':
                order.status = new_status
                order.save()
                messages.success(request, 'Order status updated successfully.')
            else:
                messages.error(request, 'Cannot update status for a cancelled order.')
                return HttpResponseBadRequest('Cannot update status for a cancelled order.')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
            return HttpResponseBadRequest('Order not found.')
    return redirect('order_list_and_detail')

def order_list_and_detail(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'order_list_and_detail.html', context)
@login_required
def user_order_view(request):
    # Admin view to display all orders
    orders = Order.objects.filter(user=request.user).all()
    context = {'orders': orders}
    return render(request, 'order_list_and_detail.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, OrderItem, Product

def cancel_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.status = 'cancelled'
    order.save()
    messages.success(request, 'Order cancelled successfully.')
    
    # Redirect to the order detail page with the order_id
    return redirect(reverse('order_detail', args=[order_id]))

def refund_order(request, order_id):
    # Get the order object or return 404 if not found
    order = get_object_or_404(Order, pk=order_id)
    
    # Check if the order status is 'cancelled' or 'refunded'
    if order.status in ['cancelled', 'refunded']:
        messages.warning(request, 'Refund cannot be processed for a cancelled or refunded order.')
    else:
        # Update the order status to 'refunded'
        order.status = 'refunded'
        order.save()
        messages.success(request, 'Order refunded successfully.')

    # Redirect to appropriate pages based on the user's role
    if request.user.is_superuser:
        # Redirect superusers to admin order view
        return redirect('order_list_and_detail')  # Update with the correct URL name for admin order view
    else:
        # Redirect regular users to their order list and detail page
        return redirect('order_list_and_detail')  # Update with the correct URL name for user order list and detail page
def order_detail(request, order_id):
    # Get the order object or return 404 if not found
    order = get_object_or_404(Order, pk=order_id)
    
    # Assuming 'items' is the related field for order items
    items = order.items.all()

    context = {'order': order, 'items': items}
    return render(request, 'order_detail.html', context)

def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('adminpage')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form, 'category': category})


@login_required
def add_product_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order = None  # Initialize order as None

    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            # Create a new review object but don't save it yet
            new_review = form.save(commit=False)
            new_review.product = product  # Associate the review with the product
            new_review.user = request.user  # Associate the review with the current user
            
            # You need to associate the review with a specific order, if applicable
            # Example logic to get the order associated with the user and product
            # Replace this with your actual logic to determine the order
            order = Order.objects.filter(user=request.user, items__product=product, status='delivered').first()
            if order:
                new_review.order = order
                new_review.save()  # Save the review to the database
                return redirect('product_detail', product_id=product_id)  # Redirect to product detail page
            else:
                # Handle case where no valid order is found
                form.add_error(None, "No valid order found for review.")  # Add a non-field error to the form

    else:
        form = ProductReviewForm()

    context = {
        'product': product,
        'form': form,
        'order': order,  # Pass the order to the template for reference if needed
    }
    return render(request, 'add_product_review.html', context)


from django.contrib.auth import views as auth_views
from django.shortcuts import render
from .forms import CustomPasswordResetForm

from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/password_reset_email.html'
    form_class = CustomPasswordResetForm  # Your custom password reset form

    def form_valid(self, form):
        # Custom logic if needed
        return super().form_valid(form)
    
from django.shortcuts import render, redirect, get_object_or_404
from .models import PurchaseOrder, PurchaseOrderItem, Product, Supplier

    

def order_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # Check if a similar order already exists for the current user and product
            existing_order = PurchaseOrder.objects.filter(user=request.user, product=product).first()
            if existing_order:
                # Update the quantity of the existing order
                existing_order.quantity += quantity
                existing_order.save()
            else:
                # Create a new order
                PurchaseOrder.objects.create(user=request.user, product=product, quantity=quantity)
            return redirect('adminpage')  # Redirect to the purchase orders page
    else:
        form = OrderForm()
    return render(request, 'order_product.html', {'form': form, 'product': product})



from .forms import SupplierForm 
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from .models import PurchaseOrder







from .models import PurchaseOrder

from django.db.models import F, Sum
def purchase_orders(request):
    purchase_orders = PurchaseOrder.objects.all()
    total_order_value = purchase_orders.aggregate(total=Sum(F('product__price') * F('quantity')))['total']
    return render(request, 'purchase_orders_list.html', {'purchase_orders': purchase_orders, 'total_order_value': total_order_value})



def supplier_purchase_orders(request):
    orders = PurchaseOrder.objects.filter(supplier=request.user.supplier_profile)
    return render(request, 'supplier_purchase_orders.html', {'orders': orders})


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags
from .models import PurchaseOrder

def send_purchase_order_email(request, order_id):
    if request.method == 'POST':
        supplier_email = request.POST.get('supplier_email')
        if not supplier_email:
            return HttpResponseBadRequest("Supplier email is missing.")
        
        try:
            order = PurchaseOrder.objects.get(id=order_id)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Invalid order ID.")
        
        subject = f'New Purchase Order #{order.id}'
        context = {
            'order_id': order.id,
            'status': order.status,
            'update_status_url': f'{settings.BASE_URL}/update_order_status/{order.id}/',
        }
        html_message = render_to_string('purchase_order_email.html', context)
        plain_message = strip_tags(html_message)  # Strip HTML tags for plain text message
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [supplier_email]
        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)
        return HttpResponse("Email sent successfully.")
    else:
        return HttpResponseBadRequest("Invalid request method.")
    


def supplier_edit(request, product_id):
    # Retrieve the product instance
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = EditProductForm(request.POST)
        if form.is_valid():
            # Get the edited quantity from the form
            edited_quantity = form.cleaned_data['quantity']
            
            # Calculate the new quantity by adding the edited quantity to the current quantity
            new_quantity = product.quantity + edited_quantity
            product.quantity = new_quantity
            product.save()

            # Remove the corresponding product from the list of purchase orders
            PurchaseOrder.objects.filter(product_id=product_id).delete()

            return redirect('supplier_dashboard')  # Redirect after editing the product
    else:
        # Pre-fill the form with the current quantity
        form = EditProductForm(initial={'quantity': product.quantity})

    return render(request, 'supplier_edit.html', {'form': form, 'product': product})

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update_product_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        order_quantity = data.get('order_quantity')
        try:
            product = Product.objects.get(pk=product_id)
            product.quantity += order_quantity
            product.save()
            return JsonResponse({'message': 'Product quantity updated successfully'}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    


@login_required
def register_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.password = (form.cleaned_data['password'])
            supplier.save()

            subject = 'Registration Successful'
            message = f"Hi {supplier.company_name},\n\nYour registration is successful. Here are your login credentials:\n\nUsername: {supplier.username}\nPassword: {form.cleaned_data['password']}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [supplier.email]
            send_mail(subject, message, email_from, recipient_list)

            return redirect('suppliers_list')  # Corrected redirection
    else:
        form = SupplierForm()
    return render(request, 'supplier_registration.html', {'form': form})

def suppliers_list(request):
    suppliers = Supplier.objects.all()  # Assuming Supplier model is imported
    return render(request, 'suppliers_list.html', {'suppliers': suppliers})
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form})
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect
from .models import Supplier  # Adjust the import as per your project structure

@csrf_protect
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, pk=supplier_id)
    if request.method == 'POST':
        supplier.delete()
        return redirect('suppliers_list')

    # Render the template with the CSRF token included
    return render(request, 'delete_supplier.html', {'supplier': supplier, 'supplier_id': supplier_id})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login



from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import SupplierForm
from django.core.mail import send_mail
from django.conf import settings


def proceed_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        # Retrieve the product from the database
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product does not exist'})

        # Update the quantity of the product
        # Example: Increase the quantity by 1
        product.quantity += 1
        product.save()

        return JsonResponse({'success': True, 'message': 'Quantity updated successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PurchaseOrder, Supplier

    
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, PurchaseOrder, Supplier
from django.contrib import messages

def reorder_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    suppliers = Supplier.objects.all()

    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        quantity = int(request.POST.get('quantity', 1))

        try:
            supplier = Supplier.objects.get(pk=supplier_id)
            PurchaseOrder.objects.create(
                user=request.user,
                product=product,
                supplier=supplier,
                quantity=quantity
            )
            messages.success(request, 'Purchase order placed successfully.')
            return redirect('adminpage')
        except Supplier.DoesNotExist:
            messages.error(request, 'Selected supplier does not exist.')
            return redirect('reorder_product', product_id=product_id)
    else:
        return render(request, 'reorder_product.html', {'suppliers': suppliers, 'product': product})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SupplierLoginForm
from django.contrib.sessions.models import Session

#supplier login
def supplier_login(request):
    if request.method == 'POST':
        form = SupplierLoginForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print('i am in ',username,password)
            user = authenticate(username=username, password=password)
            print(user  )
            if user is not None:
                print(user)
                request.session['id'] = user.id
                request.session.save()
                return redirect('supplier_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = SupplierLoginForm()

    return render(request, 'supplier_login.html', {'form': form})

from .models import PurchaseOrder, PurchaseOrderstatus
from django.db.models import F

def supplier_dashboard(request):
    supplier_id = request.session.get('id')
    if supplier_id:
        purchase_orders = PurchaseOrder.objects.filter(supplier_id=supplier_id)
        status_choices = PurchaseOrderstatus.STATUS_CHOICES
        if request.method == 'POST':
            order_id = request.POST.get('order_id')
            new_status = request.POST.get('status')
            order = PurchaseOrder.objects.get(pk=order_id, supplier_id=supplier_id)
            order.status.status = new_status
            order.status.save()

            if new_status == 'delivered':
                messages.success(request, 'Order marked as delivered. Admin will update the stock.')
            else:
                messages.success(request, 'Order status updated successfully.')

            return redirect('supplier_dashboard')
        return render(request, 'supplier_dashboard.html', {'purchase_orders': purchase_orders, 'status_choices': status_choices})
    else:
        return redirect('login_page')

def update_order_status(request, order_id):
    supplier_id = request.session.get('id')
    if supplier_id:
        order = PurchaseOrder.objects.get(pk=order_id, supplier_id=supplier_id)
        if request.method == 'POST':
            form = PurchaseOrderStatusForm(request.POST, instance=order.status)
            if form.is_valid():
                form.save()
                return redirect('supplier_dashboard')
        else:
            form = PurchaseOrderStatusForm(instance=order.status)
        return render(request, 'update_order_status.html', {'form': form})
    else:
        return redirect('login_page')
    

def admin_update_stock(request, order_id):
    order = PurchaseOrder.objects.get(pk=order_id)
    if request.method == 'POST':
        stock_quantity = int(request.POST.get('stock_quantity'))
        order.product.quantity += stock_quantity  # Increment the product quantity by the stock quantity
        order.product.save()
        messages.success(request, 'Stock updated successfully.')
        return redirect('admin_purchase_orders')
    return render(request, 'admin_update_stock.html', {'order': order})
def admin_purchase_orders(request):
    purchase_orders = PurchaseOrder.objects.all()
    return render(request, 'purchase_orders_list.html', {'purchase_orders': purchase_orders})

def update_delivered_quantity(request, order_id):
    order = get_object_or_404(PurchaseOrder, pk=order_id)
    return render(request, 'update_delivered_quantity.html', {'order': order})



from django.shortcuts import render, get_object_or_404
from .models import PurchaseOrder

def view_invoice(request, order_id):
    order = get_object_or_404(PurchaseOrder, id=order_id)
    total_price = order.product.price * order.quantity  # Calculate the total price
    context = {
        'order': order,
        'total_price': total_price,
    }
    return render(request, 'invoice.html', context)

def view_supplier_invoice(request, order_id):
    order = get_object_or_404(PurchaseOrder, id=order_id)
    return render(request, 'supplier_invoice.html', {'order': order})