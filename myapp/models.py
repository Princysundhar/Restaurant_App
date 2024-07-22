from django.db import models

# Create your models here.

class login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)

class restaurant(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    LOGIN = models.ForeignKey(login,on_delete=models.CASCADE,default=1)

class user(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE, default=1)

class rating_and_comment(models.Model):
    rating = models.CharField(max_length=100)
    review = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    USER = models.ForeignKey(user, on_delete=models.CASCADE, default=1)
    RESTAURANT = models.ForeignKey(restaurant, on_delete=models.CASCADE, default=1)

class feedback(models.Model):
    feedbacks = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    USER = models.ForeignKey(user, on_delete=models.CASCADE, default=1)

class menu(models.Model):
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    photo = models.CharField(max_length=100)
    RESTAURANT = models.ForeignKey(restaurant, on_delete=models.CASCADE, default=1)

class orderr(models.Model):
    amount = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    delivery_status = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    payment_date = models.CharField(max_length=100)
    USER = models.ForeignKey(user, on_delete=models.CASCADE, default=1)
    RESTAURANT = models.ForeignKey(restaurant, on_delete=models.CASCADE, default=1)

class order_sub(models.Model):
    quantity = models.CharField(max_length=100)
    ORDER = models.ForeignKey(orderr, on_delete=models.CASCADE, default=1)
    MENU = models.ForeignKey(menu, on_delete=models.CASCADE, default=1)



class cart(models.Model):
    quantity = models.CharField(max_length=100)
    USER = models.ForeignKey(user, on_delete=models.CASCADE, default=1)
    MENU = models.ForeignKey(menu, on_delete=models.CASCADE, default=1)

class delivery_boy(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    vehical_info = models.CharField(max_length=100)
    RESTAURANT = models.ForeignKey(restaurant, on_delete=models.CASCADE, default=1)

class allocate(models.Model):
    DELIVERY_BOY = models.ForeignKey(delivery_boy, on_delete=models.CASCADE, default=1)
    ORDER = models.ForeignKey(orderr, on_delete=models.CASCADE, default=1)

class groups(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    USER = models.ForeignKey(user, on_delete=models.CASCADE, default=1)

class group_member(models.Model):
    GROUPS = models.ForeignKey(groups, on_delete=models.CASCADE, default=1)
    USER = models.ForeignKey(user, on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=100)

class share(models.Model):
    GROUP_MEMBER = models.ForeignKey(group_member, on_delete=models.CASCADE, default=1)
    RESTAURANT = models.ForeignKey(restaurant, on_delete=models.CASCADE, default=1)
    date = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    message = models.CharField(max_length=100)








