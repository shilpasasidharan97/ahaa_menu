from website.models import Cart, ProductPortions
from website.models import CartItems
from website.models import Category
from website.models import FrontBanner
from website.models import Product
from website.models import ProductPageBanner
from website.models import Restaurant
from website.models import RestoBanner
from website.models import RestoSave
from website.models import SocialMediaLink
from website.models import SubCategory

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def _rest_id(request):
    cuser = request.session.session_key
    if not cuser:
        cuser = request.session.create()
    return cuser


def home(request, id):
    # resto = RestoSave.objects.get(user_session_id=request.session.session_key)
    rest = Restaurant.objects.get(id=id)
    categories = Category.objects.filter(restaurent=rest)
    main_banner = FrontBanner.objects.all().last()
    resto_banner = RestoBanner.objects.all().last()
    all_products = (
        Product.objects.select_related("subcategory")
        .filter(subcategory__Category__restaurent=rest)
        .values("subcategory__Category__name", "subcategory__Category__icon", "subcategory__Category__id")
        .distinct()
    )

    # try:
    #     resto_save = RestoSave.objects.get(user_session_id=_rest_id(request),resto_pk=id)
    # except RestoSave.DoesNotExist:
    #     resto_save = RestoSave.objects.create(user_session_id=_rest_id(request),resto_pk=id)
    # resto_save.save()
    if RestoSave.objects.filter(user_session_id=_rest_id(request), resto_pk=id).exists():
        resto_save = RestoSave.objects.get(user_session_id=_rest_id(request), resto_pk=id)
    else:
        resto_save = RestoSave.objects.create(user_session_id=_rest_id(request), resto_pk=id)
        resto_save.save()

    links = SocialMediaLink.objects.get(resturant=rest)
    context = {
        "categories": categories,
        "footer_banner": main_banner,
        "resto_banner": resto_banner,
        "all_products": all_products,
        # "resto":resto
        "resturants_obj": rest,
        "links": links,
    }
    return render(request, "menucard/home.html", context)


def products(request, id):
    catag = Category.objects.get(id=id)
    subcategories = SubCategory.objects.filter(is_active=True, Category=id)
    products = Product.objects.filter(subcategory__Category__id=id, is_available=True)
    product_banner = ProductPageBanner.objects.all().order_by("-id")
    # product_banner = ProductPageBanner.objects.all()[:]
    # prd = Product.objects.filter(subcategory__Category__restaurent=sub.Category.restaurent)
    catagories = Category.objects.filter(restaurent=catag.restaurent)
    resturants_obj = Restaurant.objects.get(id=catag.restaurent.id)
    links = SocialMediaLink.objects.get(resturant=resturants_obj)

    modal_banner = ProductPageBanner.objects.all().last()
    all_products = (
        Product.objects.select_related("subcategory")
        .filter(subcategory__Category__restaurent=resturants_obj)
        .values("subcategory__Category__name", "subcategory__Category__icon", "subcategory__Category__id")
        .distinct()
    )

    # if len(products) <= 10:
    if len(product_banner) >= 2:
        fist_banner = product_banner[0]
        second_banner = product_banner[1]
    elif len(product_banner) >= 1:
        fist_banner = product_banner[0]
        second_banner = product_banner[0]
    context = {
        "subcategories": subcategories,
        "products": products,
        "fist_banner": fist_banner,
        "second_banner": second_banner,
        "prd": catagories,
        "resturants_obj": resturants_obj,
        "links": links,
        "all_products": all_products,
        "modal_banner":modal_banner
    }
    return render(request, "menucard/product.html", context)
    # else :

    # context = {
    #     "subcategories":subcategories,
    #     "products":products,
    #     # "fist_banner":fist_banner,
    #     # "second_banner":second_banner,
    #     "prd":catagories,
    #     "resturants_obj":resturants_obj,
    #     "links":links,
    #     "all_products":all_products,
    # }
    # return render(request, 'menucard/product.html',context)


def productData(request, id):
    products_data = Product.objects.get(id=id)
    data = {
        "name": products_data.name,
        "price": products_data.price,
        "ingrediants": products_data.ingrediants,
        "description": products_data.description,
        "image": products_data.image.url,
    }
    return JsonResponse(data)


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def AddToCart(request, pid, qty):
    portion = request.GET['portion']
    product = Product.objects.get(id=pid)
    if portion != "full":
        item_portion = ProductPortions.objects.get(id=portion)
        size = item_portion.size
        size_price = item_portion.price
    else :
        size = "full"
        size_price = product.price
    resto = product.subcategory.Category.id
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = CartItems.objects.get(product=product, cart=cart,size=size,size_price=size_price)
        cart_item.quantity = cart_item.quantity + qty
        cart_item.save()
        total_price = float(cart_item.quantity) * float(size_price)
        cart_item.total = total_price
        cart_item.save()
        cart.save()
    except CartItems.DoesNotExist:
        cart_item = CartItems.objects.create(product=product, quantity=qty, cart=cart,size=size,size_price=size_price)
        cart_item.save()
        total_price = int(qty) * float(size_price)
        cart_item.total = total_price
        cart_item.save()
        cart.save()
    return redirect("/menucard/product/" + str(resto))


def addQuantity(request):
    quantity = request.GET["quantity"]
    id = request.GET["id"]
    cart_obj = CartItems.objects.get(id=id)
    new_quantity = int(quantity) + 1
    product_total = float(new_quantity) * float(cart_obj.size_price)
    cart_obj.total = product_total
    cart_obj.save()
    CartItems.objects.filter(id=id).update(quantity=new_quantity, total=product_total)
    data = {"total": cart_obj.total, "unitprice": cart_obj.product.price}
    return JsonResponse(data)


def lessQuantity(request):
    quantity = request.GET["quantity"]
    id = request.GET["id"]
    cart_obj = CartItems.objects.get(id=id)
    new_quantity = int(quantity) - 1
    product_total = float(new_quantity) * float(cart_obj.product.price)
    cart_obj.total = product_total
    cart_obj.save()
    CartItems.objects.filter(id=id).update(quantity=new_quantity, total=product_total)
    data = {"total": cart_obj.total, "unitprice": cart_obj.product.price}
    return JsonResponse(data)


@csrf_exempt
def tableNumber(request):
    table_name = request.POST["tablenumber"]
    messagestring = ""
    cart_obj = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItems.objects.filter(cart=cart_obj)
    tresto_number = CartItems.objects.filter(cart=cart_obj).last()
    phonenumber = tresto_number.product.subcategory.Category.restaurent.phone
    sub_total = CartItems.objects.filter(cart__cart_id=_cart_id(request)).aggregate(Sum("total"))
    data = []
    try:
        messagestring = "https://wa.me/+91" + phonenumber + "?text=Table Number :" + table_name + "%0a------Order Details------"
        for i in cart_items:
            data1 = {
                # 'id':i['id'],
                "portion":i.size,
                "name": i.product.name,
                "quantity": i.quantity,
                "price": i.size_price,
                "sub_total": i.total,
            }
            data.append(data1)
            i.delete()
            # grandtotal+=int(cart['quantity']) * int(cart['product_price'])
        for j in data:
            messagestring += (
                "%0aProduct-Name:"
                + str(j["name"])
                + "%0aPortion:"
                + str(j["portion"])
                + "%0aQuantity:"
                + str(j["quantity"])
                + "%0aUnit-Price:"
                + str(j["price"])
                + "%0aTotal :"
                + str(j["sub_total"])
                + "%0a-----------------------------"
            )
            messagestring += "%0a-----------------------------"
        messagestring += (
            "%0a-----------------------------\
        Grand Total :"
            + str(sub_total["total__sum"])
            + "%0a-----------------------------"
        )
        cart_obj.delete()
        # data = {
        #     "link":messagestring,
        # }
        # return JsonResponse(data)
    except Exception:
        pass
    data = {"link": messagestring}
    return JsonResponse(data)


def cart(request):
    # cart = Cart.objects.filter(cart_id=_cart_id(request))

    # categories = CartItems.objects.filter(cart_items__product__subcategory__Category=resto)
    cart_items = CartItems.objects.filter(cart__cart_id=_cart_id(request))
    sub_total = CartItems.objects.filter(cart__cart_id=_cart_id(request)).aggregate(Sum("total"))
    try:
        restosave_obj = RestoSave.objects.get(user_session_id=request.session.session_key)
        rest_pk = restosave_obj.resto_pk
        resturants_obj = Restaurant.objects.get(id=rest_pk)
        links = SocialMediaLink.objects.get(resturant=resturants_obj)
        all_products = (
            Product.objects.select_related("subcategory")
            .filter(subcategory__Category__restaurent=resturants_obj)
            .values("subcategory__Category__name", "subcategory__Category__icon", "subcategory__Category__id")
            .distinct()
        )
    except:
        sessions = RestoSave.objects.filter(user_session_id=request.session.session_key)
        if sessions:
            restosave_obj = sessions.last()
            resturants_obj = Restaurant.objects.get(id=restosave_obj.resto_pk)
            links = SocialMediaLink.objects.get(resturant=resturants_obj)
            all_products = (
                Product.objects.select_related("subcategory")
                .filter(subcategory__Category__restaurent=resturants_obj)
                .values("subcategory__Category__name", "subcategory__Category__icon", "subcategory__Category__id")
                .distinct()
            )
    context = {
        "cartitems": cart_items,
        "sub_total": sub_total,
        # "link":messagestring
        "resturants_obj": resturants_obj,
        "links": links,
        "all_products": all_products,
    }
    return render(request, "menucard/cart.html", context)


def orderSuccess(request):
    return render(request, "menucard/order-success.html")


def deleteCart(request, id):
    CartItems.objects.get(id=id).delete()
    return redirect("menucard:cart")
