from .models import Cart
from .models import CartItems
from .models import Category
from .models import FrontBanner
from .models import Product
from .models import ProductPageBanner
from .models import Restaurant
from .models import RestaurantQrcode
from .models import RestoSave
from .models import SocialMediaLink
from .models import SubCategory
from .models import User
from .models import Video
from django.contrib import admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone")
    search_fields = ("phone",)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant_name", "creator_name", "email", "phone")
    search_fields = ("phone",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ( "name", "id",)
    search_fields = ("name",)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("__str__", "name", "parent", "id", "category")
    search_fields = ("name",)
    autocomplete_fields = ("category","parent")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("subcategory", "name")
    search_fields = ("name",)


@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "quantity", "total")
    search_fields = ("product", "quantity", "total")


admin.site.register(RestaurantQrcode)
admin.site.register(Cart)
admin.site.register(FrontBanner)
admin.site.register(ProductPageBanner)
admin.site.register(RestoSave)
admin.site.register(Video)
admin.site.register(SocialMediaLink)
