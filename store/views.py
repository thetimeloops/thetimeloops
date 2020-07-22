from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
from math import ceil
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User , auth
from django.contrib import auth
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
import random
import json

# Create your views here.



def index(request):
    count=cart_DB.objects.filter(username=request.user.username).count()
    x_img=product_DB.objects.filter(bestseller=True)
    category=product_DB.objects.all()
    dysp_now=dyn_slide.objects.get(title="promo")
    print(dysp_now)
    return render(request,"index.html",{"count":count,"category":category,"dysp_now":dysp_now,"x_img":x_img})

def products(request,slug):
    all_product=product_DB.objects.filter(category=slug)
    product_info=product_DB.objects.filter(category=slug, bestseller=True)
    count=cart_DB.objects.filter(username=request.user.username).count()
    return render(request,"products.html",{'product_info':product_info,'all_product':all_product,'count':count})

def prodview(request,id):
    detinfo=product_DB.objects.get(product_id=id)
    return render(request,"product-page.html",{'detinfo':detinfo})


def cartadd(request):
    if request.method =="GET":
        product_id = request.GET.get('product_id','')
        slug = product_DB.objects.get(product_id=product_id)

        if cart_DB.objects.filter(product_id=product_id).exists():
            '''
            return HttpResponse(f
                <script>
                alert("Product already in your cart");
                window.location.href="products/{slug.category}"
                </script>
            )
            '''
            response = json.dumps({"logerr":"ALREADY IN CART"})
            return HttpResponse(json.dumps(response),content_type="application/json",)
        amount_data=slug.dissprice  
            
        cartitems= cart_DB(username=request.user.username,product_id=product_id,price=slug.price,category=slug.category,dissprice=slug.dissprice,cart_image=slug.front_image,amount=amount_data)
        cartitems.save()
            
        

        response = json.dumps({"logged":"DOne"})
        return HttpResponse(json.dumps(response),content_type="application/json",)
    else:
        return HttpResponse("Request method is not a GET")
    return HttpResponse("DONE")
    '''
    if request.user.is_authenticated:
        product_id = request.GET.get('product_id','')
        print(product_id)
        response = json.dumps({"sucess":"yes"})
        return HttpResponse(json.dumps(response),content_type="application/json",)
    else:
        response = json.dumps({"logerr":"Please Login"})
        return HttpResponse(json.dumps(response),content_type="application/json",)
    '''



@login_required(login_url='/login')
def cart(request):
    all_cart=cart_DB.objects.filter(username=request.user.username).order_by("-cart_add")
    return render(request,"cart.html",{'all_cart':all_cart})

@login_required(login_url='/login')
def checkout(request,id):
    slug = product_DB.objects.get(product_id=id)
    return render(request,"checkout.html",{'slug':slug})

@login_required(login_url='/login')
def placedorder(request):
    if request.method=="POST":
        product_id=request.POST.get('product_id','')
        firstname=request.POST.get('firstname','')
        lastname=request.POST.get('firstname','')
        email=request.POST.get('email','')
        adress=request.POST.get('adress','')
        city=request.POST.get('city','')
        phone=request.POST.get('phone','')
        state=request.POST.get('state','')
        zip_s=request.POST.get('zip','')
        size=request.POST.get('size','')
        quantity=request.POST.get('quantity','')
        color= request.POST.get('colors','')
        slug = product_DB.objects.get(product_id=product_id)
        

        print(size,quantity)
        amount = int(quantity) * slug.dissprice
        print(amount)

        
        placeorder_info=order_DB(username=request.user.username,email=email,firstname=firstname,lastname=lastname,address=adress,payment_type="COD",quantity=quantity,amount=amount,city=city,state=state,state_zip=zip_s,order_status="Not yet shipped",delivery_date="Next Monday",size=size,order_image=slug.front_image,product_name=slug.name)
        placeorder_info.save()
        
    order_info=order_DB.objects.filter(username=request.user.username).order_by("-order_date")
    return render(request,"orders.html",{'order_info':order_info})

@login_required(login_url='/login')
def track(request,id):
    prod=order_DB.objects.get(order_id=id)
    return render(request,"track.html",{'prod':prod})

def register(request):
    if request.method=="POST":
        user_name=request.POST.get('user_name','')
        username=request.POST.get('username','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        password=request.POST.get('password','')
        cpassword=request.POST.get('cpassword','')

        if password == cpassword:
            if User.objects.filter(email=email).exists():
                err = "Email Already exists"
                return render(request,"register.html",{'err':err})
            elif User.objects.filter(username=username).exists():
                err = "Username Taken"
                return render(request,"register.html",{'err':err})

            else:
                user_main = User.objects.create_user(username=username,password=password,email=email,first_name=user_name)
                user_main.save()
                user  =  user_DB(username=username ,name=user_name, email=email , phone=phone,password=password)
                user.save()
                return redirect("login")
        else:
            err = "Password not matching"
            return render(request,"register.html",{'err':err})

    return render(request,"register.html")


def login(request):
    if request.method=="POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request,user)

            return redirect("index")
        else:
            err= "Invalid Username or Password"
            return render(request,"login.html",{'err':err})
    else:
        return render(request,"login.html")

    return render(request.html,"login.html")

@login_required(login_url='/login')
def cartremove(request):
    product_id=request.GET.get('product_id','')
    print(product_id)
    cart_remove=cart_DB.objects.get(product_id=product_id)
    cart_remove.delete()
    return HttpResponse("BAD REQUEST 403 GO BACK")

def logout(request):
    auth.logout(request)
    return redirect("/")


def searchMatch(query, item):
    '''return true only if query matches    the item'''
    if query in item.description.lower() or query in item.name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = product_DB.objects.values('category', 'product_id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product_DB.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds': allProds, "msg": ""}
    print(params)
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'search.html', params)

def cartupdate(request):
    cart_id=request.GET.get('cart_id','')
    quantity=request.GET.get('quant_cart','')
    cart_info=cart_DB.objects.get(id=cart_id)
    print(cart_info)
    print(quantity)
    print(cart_info.amount)
    print(cart_info.quantity)

def applycode(request,id):
    product_id=product_DB.objects.get(product_id=id)
    promocode=request.GET.get('discodetext','')
    tempam=request.GET.get('tempamount','')
    print(tempam)

    if promocode_available.objects.filter(promo=promocode).exists():
        #less_amount = int(product_id.dissprice)-10
        less_amount= int(tempam)-10
        print(less_amount)
        return HttpResponse(less_amount)
    else:
        return HttpResponse("False")

def prodq(request,id):
    product_id=product_DB.objects.get(product_id=id)
    prodval = request.GET.get("prodval",'')
    print(int(prodval)*(product_id.dissprice))
    amount_total=int(prodval)*(product_id.dissprice)
    return HttpResponse(amount_total)