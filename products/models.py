from django.db import models
from categories.models import Category
from accounts.models import User


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=255)

    slug = models.SlugField(max_length=280, unique=True)

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    discount_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    stock = models.PositiveIntegerField(default=0)

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price

        return self.price
class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_code = models.CharField(
        max_length=7,
        blank=True,
        help_text="Hex code format: #FFFFFF"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="variants"
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="variants"
    )
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to="products/variants/",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("product", "color", "size")
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"

    def __str__(self):
        variant_details = []
        if self.color:
            variant_details.append(self.color.name)
        if self.size:
            variant_details.append(self.size.name)

        details = " / ".join(variant_details) if variant_details else "Default"
        return f"{self.product.name} ({details})"

    @property
    def final_price(self):
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price