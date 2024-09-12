from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count, Avg
from core.models import Product,ProductImages, Category, Vendor, CartOrder, CartOrderItems, ProductReview, Wishlists, Address  
from core.forms import ProductReviewForm
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateformat import format
from django.core import serializers



def index(request) : 
    categories = Category.objects.all()
    
    products = Product.objects.filter(product_status="published", featured=True)

    laptops_category = Category.objects.get(title='حواسيب')
    laptops = products.filter(category=laptops_category)

    phones_category = Category.objects.get(title='هواتف')
    phones = products.filter(category=phones_category)

    accessoires_category = Category.objects.get(title='أكسسوارات')
    accessoires = products.filter(category=accessoires_category)

    wishlist = Wishlists.objects.filter(user=request.user)

    context = {
        "products" : products,
        "laptops": laptops,
        "phones": phones,
        "accessoires": accessoires,
        "laptops": laptops,
        "categories": categories,
        "wishlist" : wishlist,
    }

    return render(request, 'core/index.html', context)


def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    categories = Category.objects.all()
    wishlist = Wishlists.objects.filter(user=request.user)

    context = {
        "products" : products,
        "categories" : categories,
        "wishlist" : wishlist,
    }

    return render(request, 'core/product-list.html', context)


def category_list_view(request):
    categories = Category.objects.all()
    wishlist = Wishlists.objects.filter(user=request.user)
    context = {
        "categories" : categories,
        "wishlist" : wishlist,
    }

    return render(request, 'core/category-list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)
    categories = Category.objects.all()
    wishlist = Wishlists.objects.filter(user=request.user)


    context = {
        "category":category,
        "products":products,
        "categories": categories,
        "wishlist" : wishlist,
    }

    return render(request, "core/category-product-list.html", context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()
    categories = Category.objects.all()
    wishlist = Wishlists.objects.filter(user=request.user)

    context={
        "vendors":vendors,
        "categories":categories,
        "wishlist" : wishlist,
    }

    return render(request, "core/vendor-list.html", context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")
    categories = Category.objects.all()
    wishlist = Wishlists.objects.filter(user=request.user)

    context={
        "vendor":vendor,
        "products":products,
        "categories":categories,
        "wishlist" : wishlist,
    }

    return render(request, "core/vendor-detail.html", context)

def product_detail_view(request, pid ):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    # Getting all reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Getting all reviews related to a product
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    #Product review form
    review_form = ProductReviewForm()

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0 :
            make_review = False

    categories = Category.objects.all()
    wishlist = Wishlists.objects.filter(user=request.user)
    p_images = product.p_images.all() 


    context={
        "p":product,
        "categories" : categories,
        "wishlist" : wishlist,
        "p_images" : p_images,
        "reviews" : reviews,
        "review_form" : review_form,
        "make_review" : make_review,
        "average_reviews" : average_reviews,
        "products" : products,
    }

    return render(request, "core/product-detail.html", context)

def ajax_add_review(request,pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user = user,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )

    context = {
        'user' : user.username,
        'review' : request.POST['review'],
        'rating' : request.POST['rating'],
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
            'bool' : True,
            'context' : context,
            'average_reviews' : average_reviews,
        },

    )


def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query).order_by("-date")
    categories = Category.objects.all()
    wishlist = Wishlists.objects.filter(user=request.user)


    context = {
        "products" : products,
        "query" : query,
        "categories":categories,
        "wishlist" : wishlist,

    } 
    
    return render(request, "core/search.html", context)

def add_to_cart(request):
    product_id = str(request.GET.get("id"))
    try:
        qty = int(request.GET.get("qty"))
        price = float(request.GET.get("price"))
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid quantity or price"}, status=400)

    cart_product = {
        product_id: {
            'title': request.GET.get("title"),
            'qty': qty,
            'price': price,
            'image': request.GET.get("image"),
            'pid': request.GET.get("pid"),
        }
    }

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        if product_id in cart_data:
            cart_data[product_id]['qty'] = qty
        else:
            cart_data.update(cart_product)
        request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


# def cart_view(request):
#     categories = Category.objects.all()
#     cart_total_amount = Decimal('0.00')

#     if 'cart_data_obj' in request.session:
#         cart_data = request.session['cart_data_obj']
#         for p_id, item in cart_data.items():
#             try:
#                 qty = Decimal(item['qty'])
#                 price = Decimal(item['price'])
#             except (InvalidOperation, ValueError, TypeError):
#                 qty = Decimal('0.00')
#                 price = Decimal('0.00')

#             cart_total_amount += qty * price
        
#         context = {
#             'categories': categories,
#             'cart_data': cart_data,
#             'totalcartitems': len(cart_data),
#             'cart_total_amount': cart_total_amount,
#         }

#         return render(request, "core/cart.html", context)
#     else:
#         messages.warning(request, "محفظتك فارغة")
#         return redirect("core:index")

def cart_view(request):
    categories = Category.objects.all()
    wishlist = Wishlists.objects.filter(user=request.user)

    cart_total_amount = Decimal('0.00')

    subtotal = Decimal('0.00')
    totalcartitems = 0
    cart_data = {}
    
    # Check if cart_data_obj exists in the session
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        
        for p_id, item in cart_data.items():
            try:
                qty = Decimal(item['qty'])
                price = Decimal(item['price'])
                subtotal += price * qty
            except (InvalidOperation, ValueError, TypeError):
                qty = Decimal('0.00')
                price = Decimal('0.00')

            cart_total_amount = subtotal  # Since delivery is free
            totalcartitems += 1

        # Prepare context for the template
        context = {
            'categories': categories,
            "wishlist" : wishlist,
            'cart_data': cart_data,
            'subtotal': subtotal,
            'total': cart_total_amount,
            'totalcartitems': totalcartitems,
        }

        # Render the cart page with the data
        return render(request, 'core/cart.html', context)
    else:
        # Handle empty cart case
        messages.warning(request, "محفظتك فارغة")
        return redirect("core:index")

def delete_item_from_cart(request):
    product_id = str(request.GET.get("id"))

    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        if product_id in cart_data:
            del cart_data[product_id]
            request.session['cart_data_obj'] = cart_data    #Update the session 

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in cart_data.items():
            cart_total_amount += int(item['qty']) * float (item['price'])

    context = render_to_string("core/async/cart-list.html", {
                "cart_data": request.session['cart_data_obj'],
                'totalcartitems': len(request.session['cart_data_obj']),
                'cart_total_amount': cart_total_amount
    })

    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})

    # return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})


# Checkout View
# @login_required
# def checkout_view(request):
#     cart_total_amount = 0
#     total_amount = 0
#     if 'cart_data_obj' in request.session:
        
#         # For cart Order 
#         for p_id, item in request.session['cart_data_obj'].items():
#             total_amount += int(item['qty']) * float (item['price'])

#         # Creating order object
#         order = CartOrder.objects.create(
#             user = request.user,
#             price = total_amount
#         )

#         # Getting total amount for the Cart Order Item 
#         for p_id, item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float (item['price'])

#             cart_order_items = CartOrderItems.objects.create(
#                 order = order,
#                 invoice_no = "INVOICE_NO-" + str(order.id),
#                 item = item['title'],
#                 image = item['image'],
#                 qty = item['qty'],
#                 price = item['price'],
#                 total = float(item['qty']) * float(item['price'])
#             )  


#     categories = Category.objects.all()
#     wishlist = Wishlists.objects.all()

#     # cart_total_amount = 0
#     # if 'cart_data_obj' in request.session:
#     #     for p_id, item in request.session['cart_data_obj'].items():
#     #         cart_total_amount += int(item['qty']) * float (item['price'])
        
#     return render(request, "core/checkout.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'categories':categories,"wishlist" : wishlist,} )

@login_required
def checkout_view2(request):
    wishlist = Wishlists.objects.filter(user=request.user)
    cart_total_amount = 0
    total_amount = 0
    if 'cart_data_obj' in request.session:
        
        # For cart Order 
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float (item['price'])

        # Creating order object
        order = CartOrder.objects.create(
            user = request.user,
            price = total_amount
        )

        # Getting total amount for the Cart Order Item 
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float (item['price'])

            cart_order_items = CartOrderItems.objects.create(
                order = order,
                invoice_no = "INVOICE_NO-" + str(order.id),
                item = item['title'],
                image = item['image'],
                qty = item['qty'],
                price = item['price'],
                total = float(item['qty']) * float(item['price'])
            )  


    categories = Category.objects.all()

    # cart_total_amount = 0
    # if 'cart_data_obj' in request.session:
    #     for p_id, item in request.session['cart_data_obj'].items():
    #         cart_total_amount += int(item['qty']) * float (item['price'])
        
    return render(request, "core/checkout2.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'categories':categories, "wishlist" : wishlist} )


# Save Param Infos  : NOT YET
# def save_checkout_infos(request) :
#     cart_total_amount = 0
#     total_amount = 0

#     if request.method == "POST" :
#         name = request.POST.get("name")
#         last_name = request.POST.get("last_name")
#         billing_company = request.POST.get("billing_company")
#         billing_address = request.POST.get("billing_address")
#         billing_state = request.POST.get("billing_state")
#         billing_city = request.POST.get("billing_city")
#         billing_phone = request.POST.get("billing_phone")
#         billing_email = request.POST.get("billing_email")
#         order_comments = request.POST.get("order_comments")

#         request.session['name'] = name
#         request.session['last_name'] = last_name
#         request.session['billing_company'] = billing_company
#         request.session['billing_address'] = billing_address
#         request.session['billing_state'] = billing_state
#         request.session['billing_city'] = billing_city
#         request.session['billing_phone'] = billing_phone
#         request.session['billing_email'] = billing_email
#         request.session['order_comments'] = order_comments

#         if 'cart_data_obj' in request.session:
        
#             for p_id, item in request.session['cart_data_obj'].items():
#                 total_amount += int(item['qty']) * float (item['price'])

#             order = Checkout.objects.create(
#                 user = request.user,
#                 price = total_amount,
#                 name = name,
#                 last_name = last_name,
#                 billing_company = billing_company,
#                 billing_address = billing_address,
#                 billing_state = billing_state,
#                 billing_city = billing_city,
#                 billing_phone = billing_phone,
#                 billing_email = billing_email,
#                 order_comments = order_comments,
#             )

#             del request.session['name'] 
#             del request.session['last_name'] 
#             del request.session['billing_company']  
#             del request.session['billing_address']  
#             del request.session['billing_state']  
#             del request.session['billing_city']  
#             del request.session['billing_phone']  
#             del request.session['billing_email']  
#             del request.session['order_comments'] 


#             for p_id, item in request.session['cart_data_obj'].items():
#                 cart_total_amount += int(item['qty']) * float (item['price'])

#                 cart_order_items = CartOrderItems.objects.create(
#                     order = order,
#                     invoice_no = "INVOICE_NO-" + str(order.id),
#                     item = item['title'],
#                     image = item['image'],
#                     qty = item['qty'],
#                     price = item['price'],
#                     total = float(item['qty']) * float(item['price'])
#                 )  

#         categories = Category.objects.all()


#         return redirect("core:checkout2")
#     return redirect("core:checkout2")



# Command Completed successfully
@login_required
def command_completed_view(request) :
    
    categories = Category.objects.all()
    wishlist = Wishlists.objects.filter(user=request.user)

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float (item['price'])
    
    return render(request, 'core/command-completed.html', {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'categories':categories, "wishlist" : wishlist})

@login_required
def wishlist_view(request):

    categories = Category.objects.all()
    wishlist = Wishlists.objects.filter(user=request.user)
    wishlist_count = wishlist.count()

    context = {
        "wishlist" : wishlist,
        "categories":categories,
        "wishlist_count": wishlist_count
    }
    return render(request, "core/wishlist.html", context)

@login_required
def add_to_wishlist(request):
    product_id = request.GET.get("id")
    product = Product.objects.get(id=product_id)

    context = {}

    wishlist_count = Wishlists.objects.filter(product=product, user=request.user).count()

    
    if wishlist_count > 0 :
        context = {
            "bool" : False,
            "wishlist_count": wishlist_count
        }
    else:
        new_wishlist = Wishlists.objects.create(
            product=product,
            user=request.user
        )
        wishlist_count = Wishlists.objects.filter(user=request.user).count()
        context = {
            "bool" : True,
            "wishlist_count": wishlist_count
        }

    return JsonResponse(context)

@login_required
def delete_from_wishlist(request):
    wishlist_id = request.GET.get("id")

    wishlist_item = Wishlists.objects.get(id=wishlist_id, user=request.user)
    wishlist_item.delete()

    wishlist = Wishlists.objects.filter(user = request.user)
    wishlist_count = wishlist.count()

    context = {
        "bool" : True,
        "wishlist_count" : wishlist_count
    }
    wishlist_json = serializers.serialize('json',wishlist)
    data = render_to_string("core/async/wishlist-list.html", context)

    return JsonResponse({"data": data, "wishlist":wishlist_json})