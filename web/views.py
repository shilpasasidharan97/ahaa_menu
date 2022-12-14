from aahalive.decorators import auth_restaurant
from website.models import Category
from website.models import Product
from website.models import Restaurant
from website.models import RestaurantQrcode
from website.models import RestoBanner
from website.models import SocialMediaLink
from website.models import SubCategory
from website.models import User, ProductPortions

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render


# Create your views here.


@auth_restaurant
@login_required(login_url="/official/login-page")
def home(request):
    user = request.user
    qr_code = RestaurantQrcode.objects.get(restaurant=user.restaurant)
    category_count = Category.objects.filter(restaurent=user.restaurant).count()
    product_count = Product.objects.filter(subcategory__Category__restaurent=user.restaurant).count()
    all_product = Product.objects.filter(subcategory__Category__restaurent=user.restaurant)[:5]
    context = {"is_home": True, "qr_code": qr_code, "category_count": category_count, "product_count": product_count, "all_product": all_product}
    return render(request, "web/home.html", context)


@auth_restaurant
@login_required(login_url="/official/login-page")
def category(request):
    categories = Category.objects.filter(restaurent=request.user.restaurant)
    if request.method == "POST":
        category_name = request.POST["cat-name"]
        category_image = request.FILES["cat-image"]
        new_category = Category(name=category_name, icon=category_image, restaurent=request.user.restaurant)
        new_category.save()
    else:
        pass
    context = {"is_product": True, "categories": categories}
    return render(request, "web/category.html", context)


def categoryNameValidation(request):
    category = request.GET["cat_name"]
    if Category.objects.filter(name=category).exists():
        data = {"msg": "Category alerdy exists"}
        return JsonResponse(data)
    else:
        data = {"sss": "sss"}
        return JsonResponse(data)


def getCategory(request, id):
    category = Category.objects.get(id=id)
    data = {"name": category.name, "image": category.icon.url}
    return JsonResponse(data)


def editCategory(request):
    cname = request.POST["name"]
    print(cname, "name" * 10)
    image = request.FILES.get("photo", "Photo Not Uploded")
    print(image, "image" * 20)
    id = request.POST["fid"]
    print(id, "id" * 20)

    cat = Category.objects.get(id=id)
    cat.name = cname
    Category.objects.filter(id=id).update()
    if image != "Photo Not Uploded":
        cat.icon = image
        cat.save()
    else:
        pass
    return JsonResponse({"data": "sss"})


def deleteCategory(request, id):
    catagory = Category.objects.get(id=id)
    catagory.delete()
    return redirect("web:category")


@auth_restaurant
@login_required(login_url="/official/login-page")
def subCategory(request, id):
    subcategories = SubCategory.objects.filter(Category__restaurent=request.user.restaurant, Category=id)
    category = Category.objects.get(id=id)
    if request.method == "POST":
        subcat_name = request.POST["subcat-name"]
        new_subactegory = SubCategory(name=subcat_name, Category=category)
        new_subactegory.save()
    context = {"is_product": True, "subcategories": subcategories}
    return render(request, "web/subcategory.html", context)


def getSubcategory(request, id):
    subcategory = SubCategory.objects.get(id=id)
    print(subcategory)
    data = {"name": subcategory.name}
    print(data)
    return JsonResponse(data)


def deleteSubCategory(request, id):
    catagory = SubCategory.objects.get(id=id)
    catagory.delete()
    return redirect("/web/subcategory/" + str(catagory.Category.id))


@auth_restaurant
@login_required(login_url="/official/login-page")
def product(request, id):
    products = Product.objects.filter(subcategory__Category__restaurent=request.user.restaurant, subcategory=id)
    # print(products)
    subCategory = SubCategory.objects.get(id=id)
    if request.method == "POST":
        product_name = request.POST["p_name"]
        product_price = request.POST["p_price"]
        product_ingrediants = request.POST["p_ingrediants"]
        product_description = request.POST["p_descriptions"]
        product_image = request.FILES["p_image"]
        portion = request.POST['portion']
        new_product = Product(name=product_name, price=product_price, ingrediants=product_ingrediants, description=product_description, image=product_image, subcategory=subCategory
        )
        new_product.save()
        if portion == "available":
            if request.POST['quaterprice'] != "" :
                quater_price =  request.POST['quaterprice']
            else :
                quater_price = new_product.price
            if request.POST['halfprice'] != "" :
                half_price =  request.POST['halfprice']
            else :
                half_price =  new_product.price
            
            qportion = ProductPortions(product=new_product,size="Quater",price=quater_price)
            qportion.save()
            hproduct = ProductPortions(product=new_product,size="Half",price=half_price)
            hproduct.save()
    context = {"is_product": True, "products": products, "id": subCategory.Category.id}
    return render(request, "web/product.html", context)


def productNotavailable(request, id):
    product = Product.objects.get(id=id)
    cat = product.subcategory.id
    Product.objects.filter(id=id).update(is_available=False)
    return redirect("/web/product/" + str(cat))


def productavailable(request, id):
    product = Product.objects.get(id=id)
    cat = product.subcategory.id
    Product.objects.filter(id=id).update(is_available=True)
    return redirect("/web/product/" + str(cat))


def deleteProduct(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("/web/product/" + str(product.subcategory.id))


# product show modal
def productshow(request, id):
    product = Product.objects.get(id=id)
    data = {"name": product.name, "price": product.price, "ingrediants": product.ingrediants, "description": product.description, "image": product.image.url}
    return JsonResponse(data)


@auth_restaurant
@login_required(login_url="/official/login-page")
def banner(request):
    all_banner = RestoBanner.objects.filter(resto=request.user.restaurant).all()
    if request.method == "POST":
        resto_banner = request.FILES["home-image"]
        new_banner = RestoBanner(image=resto_banner, resto=request.user.restaurant)
        new_banner.save()
    context = {"is_banner": True, "all_banner": all_banner}
    return render(request, "web/banner.html", context)


@auth_restaurant
@login_required(login_url="/official/login-page")
def profile(request):
    profile_data = Restaurant.objects.get(id=request.user.restaurant.id)
    print(profile_data)
    context = {"is_profile": True, "profile_data": profile_data}
    return render(request, "web/profile.html", context)


@auth_restaurant
@login_required(login_url="/official/login-page")
def settings(request):
    resto_data = Restaurant.objects.get(id=request.user.restaurant.id)
    if request.method == "POST":
        cname = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        location = request.POST["location"]
        state = request.POST["state"]
        address = request.POST["address"]
        password = request.POST["password"]
        Restaurant.objects.filter(id=request.user.restaurant.id).update(
            restaurant_name=cname, email=email, phone=phone, district=location, state=state, address=address, password=password
        )
        # get_user_model().objects.filter(id=request.user.restaurant.id).update(email=email,phone=phone)
        user = User.objects.get(restaurant=request.user.restaurant)
        user.set_password(password)
        user.save()
        get_user_model().objects.filter(id=request.user.id).update(email=email, phone=phone)
    context = {"is_settings": True, "resto_data": resto_data}
    return render(request, "web/settings.html", context)


# SOCIAL MEDIA LINKS
def socialMedialinks(request):
    all_links = SocialMediaLink.objects.get(resturant=request.user.restaurant)
    # print(all_links.facebook)
    if request.method == "POST":
        facebook = request.POST["facebook"]
        instagram = request.POST["instagram"]
        whatsapp = request.POST["whatsapp"]
        location = request.POST["location"]

        SocialMediaLink.objects.filter(resturant=request.user.restaurant).update(facebook=facebook, instagram=instagram, whatsapp=whatsapp, location=location)
        return redirect("web:socialmedia")

    context = {"is_links": True, "all_links": all_links}

    return render(request, "web/social_media.html", context)


# table
def tableOff(request, id):
    Restaurant.objects.filter(id=id).update(is_table=False)
    return redirect("web:home")


def tableOn(request, id):
    Restaurant.objects.filter(id=id).update(is_table=True)
    return redirect("web:home")
