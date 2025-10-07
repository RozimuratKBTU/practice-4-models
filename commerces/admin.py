from django.contrib import admin
from .models import Address, Order, OrderItem, OrderItemOption, PromoCode, OrderPromo

class OrderItemOptionInline(admin.TabularInline):
    model = OrderItemOption
    extra = 0

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderPromoInline(admin.TabularInline):
    model = OrderPromo
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'status', 'total', 'created_at')
    inlines = [OrderItemInline, OrderPromoInline]

@admin.register(PromoCode)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('code', 'active', 'expires_at')