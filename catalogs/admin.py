from django.contrib import admin
from .models import Restaurant, Category, Option, MenuItem, ItemCategory, ItemOption

class ItemCategoryInline(admin.TabularInline):
    model = ItemCategory
    extra = 1

class ItemOptionInline(admin.TabularInline):
    model = ItemOption
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'base_price', 'available')
    inlines = [ItemCategoryInline, ItemOptionInline]

admin.site.register(Category)
admin.site.register(Option)