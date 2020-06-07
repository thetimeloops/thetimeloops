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
    path('search',views.search,name="search")
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
