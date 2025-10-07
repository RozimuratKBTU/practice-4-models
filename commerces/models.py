from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

from django.utils.translation.trans_real import catalog

User = settings.AUTH_USER_MODEL


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField(max_length=120, blank=True)
    line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=80, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def str(self):
        return f"{self.label or self.line1} ({self.user})"


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONFIRMED = "confirmed", "Confirmed"
        DELIVERING = "delivering", "Delivering"
        DONE = "done", "Done"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey("catalogs.Restaurant", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                   validators=[MinValueValidator(0)])
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                         validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                validators=[MinValueValidator(0)])

    promocodes = models.ManyToManyField('PromoCode', through='OrderPromo', related_name='orders', blank=True)

    def str(self):
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menuitem = models.ForeignKey('catalogs.MenuItem', null=True, blank=True, on_delete=models.SET_NULL)
    item_name = models.CharField(max_length=200)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        # Ensure line_total matches price*quantity if not set
        if not self.line_total:
            self.line_total = self.item_price * self.quantity
        super().save(*args, **kwargs)

    def str(self):
        return f"{self.quantity}x {self.item_name}"


class OrderItemOption(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='selected_options')
    option_name = models.CharField(max_length=200)
    price_delta = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def str(self):
        return f"{self.option_name} for {self.order_item}"


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                          validators=[MinValueValidator(0)])
    discount_percent = models.PositiveSmallIntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def str(self):
        return self.code


class OrderPromo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    promocode = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    applied_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                         validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('order', 'promocode')

    def str(self):
        return f"{self.promocode} applied to {self.order}"
