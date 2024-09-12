from django.urls import path
from core.views import ajax_add_review, category_product_list_view, index, product_detail_view, product_list_view, category_list_view, vendor_list_view, vendor_detail_view,search_view,add_to_cart,cart_view, delete_item_from_cart,command_completed_view, checkout_view2, wishlist_view, add_to_wishlist, delete_from_wishlist

app_name = "core"

urlpatterns = [
    path("", index, name="index"),

    # Product list url
    path("products/", product_list_view, name="product-list"),

    # Product detail url
    path("product/<pid>/", product_detail_view, name="product-detail"),

    # category list url
    path("category/", category_list_view, name="category-list"),

    # category product list url

    path("category/<cid>/", category_product_list_view, name="category-product-list"),

    # vendor list url
    path("vendors/", vendor_list_view, name="vendor-list"),

    # vendor details url
    path("vendor/<vid>/", vendor_detail_view, name="vendor-detail"),

    # Add Review
    path("ajax-add-review/<int:pid>/", ajax_add_review, name="ajax-add-review"),
    
    # Search 
    path("search/", search_view, name="search"),

    # Add to cart 
    path("add-to-cart/", add_to_cart, name="add-to-cart"),

    # Cart Page url
    path("cart/", cart_view, name="cart"),

    # delete item from cart
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),

    # Checkout page
    # path("checkout/", checkout_view, name="checkout"),
    path("checkout2/", checkout_view2, name="checkout2"),

    # Command Completed successfully
    path("command-completed/", command_completed_view, name="command-completed"),

    # Wishlists
    path("wishlist/", wishlist_view, name="wishlist"),

    # Add product to wishlist 
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),

    # Remove product from wishlist 
    path("remove-from-wishlist/", delete_from_wishlist, name="remove-from-wishlist")

]
