from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse

# Create your models here.

User = get_user_model()



class ColorVariation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class SizeVariation(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

class Address(models.Model):
    ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    county = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    phone_number1 = models.IntegerField()
    phone_number2 = models.IntegerField()
    Address_type = models.CharField(max_length=1, null=True, choices= ADDRESS_CHOICES)


    def __str__(self):
        return f"{self.phone_number1}, {self.phone_number2} "

    class Meta:
        verbose_name_plural = 'Addresses'


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="product_images", null=True)
    description = models.TextField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    available_colours = models.ManyToManyField(ColorVariation)
    available_sizes = models.ManyToManyField(SizeVariation)

    def __str__(self):
        return f"{self.name}, {self.created}"

    def get_absolute_url(self):
        return reverse("cart:product-detail", kwargs={'slug': self.slug})

    def get_price(self):
        return "{:.2f}".format(self.price/100)

class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, related_name='user', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)

    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='bills', blank=True, null=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='shipp', blank=True, null=True)

    def def__str__(self):
        return reference_number

    @property
    def reference_number(self):
        return f"Order-{self.pk}"

    def get_raw_subtotal(self):
        total = 0

        for order_item in self.items.all():
            total += order_item.get_raw_total()
        return total
    
    def get_subtotal(self):
        sub = self.get_raw_subtotal()

        return "{: .2f}".format(sub/100)


class OrderItem(models.Model):
    quantity = models.IntegerField(default=1)
    product = models.ForeignKey(Product, related_name='item', on_delete = models.CASCADE)
    order = models.ForeignKey(Order, related_name='items', on_delete = models.CASCADE)
    color = models.ForeignKey(ColorVariation, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeVariation, on_delete=models.CASCADE)

    def def__str__(self):
        return f"{self.quantity}"
    def get_raw_total(self):
        return self.quantity*self.product.price

    def get_item_total(self):
        price = self.get_raw_total()
        return "{: .2f}".format(price/100)
    





class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=1, choices=(('p', 'paypal'), ('m', 'mpesa')))
    time_stamp = models.DateTimeField(auto_now_add=True)
    succesful= models.BooleanField(default=False)
    amount = models.FloatField()
    raw_response = models.TextField()

    def def__str__(self):
        return reference_number

    @property
    def reference_number(self):
        return f"PAYMENT-{self.pk}-{self.order}"

def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
pre_save.connect(pre_save_product_receiver, sender=Product)



    


