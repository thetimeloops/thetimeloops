from django.db import models

# Create your models here.

size_choice=( 
    ("S", "S"), 
    ("M", "M"), 
    ("L", "L"),
    ("XL","XL"), 
 ) 


gender_choice=(
    ("Kid", "Kid"), 
    ("Male", "Male"), 
    ("Female", "Female"),
)



class product_DB(models.Model):
    product_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=1000)
    price=models.IntegerField()
    category=models.CharField(max_length=100,choices=gender_choice)
    dissprice=models.IntegerField()
    description=models.TextField()
    size=models.CharField(max_length=20,choices=size_choice,default="M")
    new=models.BooleanField(default=False)
    bestseller=models.BooleanField(default=False)
    outofstock=models.BooleanField(default=False)
    fewleft=models.BooleanField(default=False)
    front_image=models.ImageField(blank=True,upload_to='prodimages/')
    back_image=models.ImageField(blank=True,upload_to='prodimages/')
    model_image=models.ImageField(blank=True,upload_to='prodimages/')

    def __str__(self):
        return self.name

class cart_DB(models.Model):
    username=models.CharField(max_length=1000)
    product_id=models.CharField(max_length=100)
    price=models.IntegerField()
    category=models.CharField(max_length=100,choices=gender_choice)
    dissprice=models.IntegerField()
    cart_image=models.ImageField(blank=True)

    def __str__(self):
        return self.username

class order_DB(models.Model):
    order_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=1000,default="")
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    product_id=models.CharField(max_length=100)
    name=models.CharField(max_length=1000)
    size=models.CharField(max_length=20)
    address=models.CharField(max_length=1000)
    phone=models.CharField(max_length=20)
    payment_type=models.CharField(max_length=20)
    quantity=models.IntegerField()
    amount=models.IntegerField()
    state_zip=models.CharField(max_length=1000)
    order_date=models.DateTimeField(auto_now_add=True)
    ordered=models.BooleanField(default=False)
    cancelled=models.BooleanField(default=False)
    processing=models.BooleanField(default=True)
    order_status=models.CharField(max_length=1000)
    delivery_date=models.CharField(max_length=100,blank=True)
    order_image=models.ImageField(blank=True)

    def __str__(self):
        return self.username    

class user_DB(models.Model):
    name= models.CharField(max_length=100)
    username=models.CharField(max_length=200)
    phone=models.CharField(max_length=11)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.username
 

class dyn_slide(models.Model):
    dyn_img1=models.ImageField(blank=True,upload_to='dynamic_images/')
    dyn_img2=models.ImageField(blank=True,upload_to='dynamic_images/')
    dyn_img3=models.ImageField(blank=True,upload_to='dynamic_images/')
    dysp=models.BooleanField(default=False)
    title=models.CharField(max_length=20)

    def __str__(self):
        return self.title

class promocode_available(models.Model):
    promo=models.CharField(max_length=30)

    def __str__(self):
        return self.promo
class promocode_used(models.Model):
    promo_txt=models.CharField(max_length=30)
    date_used=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.promo_txt
        


