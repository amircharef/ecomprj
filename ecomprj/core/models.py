from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from ckeditor_uploader.fields import RichTextUploadingField



STATUS_CHOICE = (
    ("Processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)


RATING = (
    (1, "⭑⭒⭒⭒⭒"),
    (2, "⭑⭑⭒⭒⭒"),
    (3, "⭑⭑⭑⭒⭒"),
    (4, "⭑⭑⭑⭑⭒"),
    (5, "⭑⭑⭑⭑⭑"),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(
        unique=True,
        length=10,
        max_length=30,
        prefix="cat",
        alphabet="abcdefgh12345"
    )
    title = models.CharField(max_length=100, default="Computer")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField(
        unique=True,
        length=10,
        max_length=30,
        prefix="ven",
        alphabet="abcdefgh12345"
    )
    title = models.CharField(max_length=100, default="Vendor")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    # description = models.TextField(null=True, blank=True, default="I am an Amazing vendor")
    description = RichTextUploadingField(null=True, blank=True, default="I am an Amazing vendor")

    address = models.CharField(max_length=100, default="Khenchela")
    contact = models.CharField(max_length=100, default="0555555555")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Vendor"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

class Product(models.Model):
    pid = ShortUUIDField(
        unique=True,
        length=10,
        max_length=30,
        alphabet="abcdefgh12345"
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="vendor")
    
    title = models.CharField(max_length=100, default="CS")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    # description = models.TextField(null=True, blank=True, default="This is the product")
    description = RichTextUploadingField(null=True, blank=True, default="This is the product")

    price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default="2.99")

    # specifications = models.TextField(null=True, blank=True, default="Good Product !")
    specifications = RichTextUploadingField(null=True, blank=True, default="Good Product !")
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    stock_count = models.CharField(max_length=100, default="8", null=True, blank=True)


    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    degital = models.BooleanField(default=False)

    sku = ShortUUIDField (
        unique=True,
        length=4,
        max_length=10,
        prefix="sku",
        alphabet="abcdefgh1234567890"
    )

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_percentage(self):
        if self.old_price == 0:
            return 0
        new_price = ((self.old_price - self.price) / self.old_price) * 100
        return new_price


class ProductImages(models.Model): 
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="p_images")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

################################ Cart, Order, orderItel and @ ###########
################################ Cart, Order, orderItel and @ ###########
################################ Cart, Order, orderItel and @ ###########
################################ Cart, Order, orderItel and @ ###########
################################ Cart, Order, orderItel and @ ###########
################################ Cart, Order, orderItel and @ ###########



class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="Processing")

    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    total = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")

    class Meta:
        verbose_name_plural = "Cart Order Item"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

################################ Product, Review, Wishlists, @ ###########
################################ Product, Review, Wishlists, @ ###########
################################ Product, Review, Wishlists, @ ###########
################################ Product, Review, Wishlists, @ ###########
################################ Product, Review, Wishlists, @ ###########
################################ Product, Review, Wishlists, @ ###########

class ProductReview(models.Model): 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products Reviews"

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating

# class Checkout(models.Model) :
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
#     paid_status = models.BooleanField(default=False)
#     order_date = models.DateTimeField(auto_now_add=True)
#     product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="Processing")
#     name = models.CharField(max_length=100, null=True, blank=True)
#     last_name = models.CharField(max_length=100, null=True, blank=True)
#     billing_company = models.CharField(max_length=100, null=True, blank=True)
#     billing_address = models.CharField(max_length=100, null=True, blank=True)
#     billing_state = models.CharField(max_length=100, null=True, blank=True)
#     billing_city = models.CharField(max_length=100, null=True, blank=True)
#     billing_phone = models.CharField(max_length=100, null=True, blank=True)
#     billing_email = models.CharField(max_length=100, null=True, blank=True)
#     order_comments = models.CharField(max_length=100, null=True, blank=True)
#     shipping_method = models.CharField(max_length=100, null=True, blank=True)


#     class Meta:
#         verbose_name_plural = "Checkout "


class Wishlists(models.Model): 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists "

    def __str__(self):
        return self.product.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"
