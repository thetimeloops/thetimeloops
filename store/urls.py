from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('',views.index,name="index"),
    path('products/<str:slug>',views.products,name="products"),
    path('prodview/<int:id>',views.prodview,name="prodview"),
    path('cartadd',views.cartadd,name="cartadd"),
    path('cart',views.cart,name="cart"),
    path('checkout/<int:id>',views.checkout,name="checkout"),
    path('placedorder',views.placedorder,name="placedorder"),
    path('track/<int:id>',views.track,name="views"),
    path('register',views.register,name="register"),
    path('login',views.login,name="login"),
    path('cartremove',views.cartremove,name="cartremove"),
    path('logout',views.logout,name="logout"),
    path('search',views.search,name="search"),
    path('cartupdate',views.cartupdate,name="cartupdate"),
    path('applycode/<int:id>',views.applycode,name="applycode"),
    path('orders',views.placedorder,name="orders"),
    path('prodq/<int:id>',views.prodq,name="prodq")
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
