from django.db import models
from django.core.validators import MinValueValidator

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=False, blank=True, null=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    def str(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True, null=True)

    def str(self):
        return self.name

class Option(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)

    def str(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menuitems')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    available = models.BooleanField(default=True)

    categories = models.ManyToManyField(Category, through='ItemCategory', related_name='menuitems')
    options = models.ManyToManyField(Option, through='ItemOption', related_name='menuitems')

    def str(self):
        return f"{self.name} ({self.restaurant})"

class ItemCategory(models.Model):
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('menuitem', 'category')
        ordering = ['position']

    def str(self):
        return f"{self.menuitem} in {self.category} pos {self.position}"

class ItemOption(models.Model):
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    price_delta = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ('menuitem', 'option')

    def str(self):
        return f"{self.option} for {self.menuitem}"