from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
from math import ceil
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User , auth
from django.contrib import auth
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    count=cart_DB.objects.filter(username=request.user.username).count()
    return render(request,"home-page.html",{'count':count})

def products(request,slug):
    product_info=product_DB.objects.filter(category=slug)
    count=cart_DB.objects.filter(username=request.user.username).count()
    return render(request,"products.html",{'product_info':product_info,'count':count})

def prodview(request,id):
    detinfo=product_DB.objects.get(product_id=id)
    return render(request,"product-page.html",{'detinfo':detinfo})

@login_required(login_url='/login')
def cartadd(request):
    if request.method =="POST":
        product_id = request.POST.get('product_id','')
        slug = product_DB.objects.get(product_id=product_id)
        
        if cart_DB.objects.filter(product_id=product_id).exists():
            return HttpResponse(f'''
                <script>
                alert("Product already in your cart");
                window.location.href="products/{slug.category}"
                </script>
            ''')
        cartitems= cart_DB(username=request.user.username,product_id=product_id,price=slug.price,category=slug.category,dissprice=slug.dissprice,cart_image=slug.front_image)
        cartitems.save()
        
        
        return redirect(f'products/{slug.category}')
    else:
        return HttpResponse("Request method is not a GET")
    return HttpResponse("DONE")

@login_required(login_url='/login')
def cart(request):
    all_cart=cart_DB.objects.filter(username=request.user.username)
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
        email=request.POST.get('email','')
        adress=request.POST.get('adress','')
        state=request.POST.get('state','')
        zip_s=request.POST.get('zip','')
        size=request.POST.get('size','')
        quantity=request.POST.get('quantity','')
        slug = product_DB.objects.get(product_id=product_id)

        amount = int(slug.dissprice)*int(quantity)

        print(size,amount)

        
        placeorder_info=order_DB(username=request.user.username,email=email,name=firstname,address=adress,payment_type="COD",quantity=quantity,amount=amount,state_zip=zip_s,order_status="Not yet shipped",delivery_date="Next Monday",size=size,order_image=slug.front_image,product_name=slug.name)

        placeorder_info.save()
        
    order_info=order_DB.objects.filter(username=request.user.username)
    return render(request,"placedorder.html",{'order_info':order_info})
    
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
    if request.method=="POST":
        product_id=request.POST.get('product_id','')
        cart_remove=cart_DB.objects.get(product_id=product_id)
        cart_remove.delete()
        return redirect('cart')
    return HttpResponse("BAD REQUEST 403 GO BACK")

def logout(request):
    auth.logout(request)
    return redirect("/")


def searchMatch(query, item):
    '''return true only if query matches the item'''
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