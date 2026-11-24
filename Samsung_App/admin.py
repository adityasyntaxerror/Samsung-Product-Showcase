from django.contrib import admin

from .models import Category, Product, SiteImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "is_featured", "image_url")
    list_editable = ("is_featured", "image_url")
    list_filter = ("category", "is_featured")
    search_fields = ("title", "tagline")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    list_display = ("key", "url", "alt")
    list_editable = ("url", "alt")
