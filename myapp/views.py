import datetime
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, Q
from django.db.models.expressions import RawSQL
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *

# Create your views here.

#==============================================================================

def log(request):
    return render(request,"login_index.html")

def log_post(request):
    username = request.POST['textfield']
    password = request.POST['textfield2']
    data = login.objects.filter(username=username,password=password)
    if data.exists():
        data = data[0]
        request.session['lid'] = data.id
        request.session['lg'] = "lin"
        if data.usertype == 'admin':
            return HttpResponse("<script>alert('Login Success');window.location='/admin_home'</script>")
        elif data.usertype == 'restaurant':
            return HttpResponse("<script>alert('Welcome to restaurant home');window.location='/restaurant_home'</script>")
        else:
            return HttpResponse("<script>alert('wait for authentication!!!');window.location='/'</script>")

    else:
        return HttpResponse("<script>alert('Invalid');window.location='/'</script>")

def admin_home(request):
    return render(request,"admin/admin_index.html")

def restaurant_home(request):
    return render(request,"restaurant/restaurant_index.html")

def logout(request):
    request.session['lg'] =""
    return HttpResponse("<script>alert('Logout Successfully');window.location='/'</script>")

def forgot_password(request):
    return render(request,"forgot_password.html")

def forgot_password_post(request):
    email = request.POST['textfield2']
    data = login.objects.filter(username=email)
    if data.exists():
        pwd = data[0].password
        import smtplib

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("demo@gmail.com", "tcap lzzh lmrz afio")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "demo@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for Rent a home Website"
        body = "Your Password is:- - " + str(pwd)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        return HttpResponse("<script>alert('password sended');window.location='/'</script>")

    return HttpResponse("mail incorrect")


#======================= ADMIN MODULE ========================

def change_password(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "CHANGE PASSWORD"
    return render(request,"admin/change_password.html")

def change_password_post(request):
    old = request.POST['textfield']
    new = request.POST['textfield2']
    confirm = request.POST['textfield3']
    res = login.objects.filter(password=old,id=request.session['lid'])
    if res.exists():
        if new == confirm:
            login.objects.filter(id=request.session['lid']).update(password=confirm)
            return HttpResponse("<script>alert('Password updated');window.location='/change_password'</script>")
        else:
            return HttpResponse("<script>alert('Password mismatch');window.location='/change_password'</script>")
    else:
        return HttpResponse("<script>alert('Doesnt Exists!! ');window.location='/change_password'</script>")

def admin_view_restaurant(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VERIFY RESTAURANT"
    data = restaurant.objects.filter(LOGIN__usertype='pending')
    return render(request,"admin/verify_restaurant.html",{"data":data})

def approve_restaurnant(request,id):
    login.objects.filter(id=id).update(usertype='restaurant')
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('demo@gmail.com', 'vile vivc hvnh xdgs')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("Restaurant App")
    msg['Subject'] = 'Verification'
    msg['To'] = email
    msg['From'] = 'demo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    return HttpResponse("<script>alert('Approved!check your Email');window.location='/admin_view_restaurant'</script>")


def reject_restaurnant(request,id):
    login.objects.filter(id=id).update(usertype='reject')
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('demo@gmail.com', 'vile vivc hvnh xdgs')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("Restaurant App")
    msg['Subject'] = 'Verification'
    msg['To'] = email
    msg['From'] = 'demo@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    # return redirect('/admin_view_restaurant#aaa')
    return HttpResponse("<script>alert('Rejected!check your Email');window.location='/admin_view_restaurant'</script>")

def admin_view_verified_restaurant(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VERIFED RESTAURANT"
    data = restaurant.objects.filter(LOGIN__usertype='restaurant')
    return render(request,"admin/view_verified_restaurant.html",{"data":data})

def view_restaurant_rating(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW RATING"
    res = rating_and_comment.objects.filter(RESTAURANT_id=id)
    fs = "/static/star/full.jpg"
    hs = "/static/star/half.jpg"
    es = "/static/star/empty.jpg"
    data = []

    for rt in res:
        a = float(rt.rating)

        if a >= 0.0 and a < 0.4:
            ar = [es, es, es, es, es]
            data.append(
                {
                    "rating": ar,
                    "review":rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )

        elif a >= 0.4 and a < 0.8:
            ar = [hs, es, es, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 0.8 and a < 1.4:
            ar = [fs, es, es, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 1.4 and a < 1.8:
            ar = [fs, hs, es, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 1.8 and a < 2.4:
            ar = [fs, fs, es, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 2.4 and a < 2.8:
            ar = [fs, fs, hs, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 2.8 and a < 3.4:
            ar = [fs, fs, fs, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 3.4 and a < 3.8:
            ar = [fs, fs, fs, hs, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 3.8 and a < 4.4:
            ar = [fs, fs, fs, fs, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 4.4 and a < 4.8:
            ar = [fs, fs, fs, fs, hs]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 4.8 and a <= 5.0:
            ar = [fs, fs, fs, fs, fs]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )
    return render(request, "admin/view_rating.html", {"data": data})

def admin_view_user(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW USER"
    data = user.objects.all()
    return render(request,"admin/view_user.html",{"data":data})

def admin_view_feedback(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW FEEDBACK"
    data = feedback.objects.all()
    return render(request,"admin/view_feedback.html",{"data":data})

def admin_view_delivery_boy(request,id):
    data = delivery_boy.objects.filter(RESTAURANT_id=id)
    return render(request,"admin/view_delivery_boy.html",{"data":data})

def view_payment(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW PAYMENT"
    return render(request,"admin/view_payment.html")

def view_payment_post(request):
    month = request.POST['select']
    year = request.POST['select2']

    month_mapping = {
        "January": "01", "Februvary": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08",
        "september": "09", "october": "10", "november": "11", "december": "12"
    }

    month_number = month_mapping.get(month, "00")
    formatted_date = f"{year}-{month_number}"
    res = order_sub.objects.filter(ORDER__payment_date__startswith=formatted_date).aggregate(total_amount=Sum('ORDER__amount'))
    data = [{
        "total_amount": res.get('total_amount') or 0
    }]

    return render(request, "admin/view_payment.html", {"data": data})


#=========================== RESTAURANT MODULE =====================================

def register(request):
    return render(request,"restaurant/Registeration.html")

def register_post(request):
    name = request.POST['textfield']
    email = request.POST['textfield2']
    contact = request.POST['textfield3']
    latitude = request.POST['textfield8']
    longitude = request.POST['textfield9']
    password = request.POST['textfield6']
    image = request.FILES['image']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\DELL\PycharmProjects\RestaurantApp\myapp\static\Restaurants\\" + dt + '.jpg', image)
    path = '/static/Restaurants/' + dt + '.jpg'
    data = login.objects.filter(username=email)
    if data.exists():
        return HttpResponse("<script>alert('Already Registered');window.location='/'</script>")
    else:
        obj = login()
        obj.username = email
        obj.password = password
        obj.usertype = "pending"
        obj.save()

        obj1 = restaurant()
        obj1.name = name
        obj1.email = email
        obj1.contact = contact
        obj1.latitude = latitude
        obj1.longitude = longitude
        obj1.image = path
        obj1.LOGIN = obj
        obj1.save()
        return HttpResponse("<script>alert('Registeration success!');window.location='/'</script>")

# === MENU MANAGEMENT =============

def add_menu(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "ADD MENU"
    return render(request,"restaurant/add_menu.html")

def add_menu_post(request):
    name = request.POST['textfield']
    amount = request.POST['textfield2']
    image = request.FILES['fileField']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\DELL\PycharmProjects\RestaurantApp\myapp\static\menu\\" + dt + '.jpg', image)
    path = '/static/menu/' + dt + '.jpg'
    data = menu.objects.filter(name=name)
    if data.exists():
        return HttpResponse("<script>alert('Already Added,Try another');window.location='/add_menu#aaa'</script>")
    else:
        obj = menu()
        obj.name = name
        obj.amount = amount
        obj.photo = path
        obj.RESTAURANT = restaurant.objects.get(LOGIN=request.session['lid'])
        obj.save()
        return HttpResponse("<script>alert('success!');window.location='/add_menu#aaa'</script>")

def view_menu(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW MENU"
    data = menu.objects.filter(RESTAURANT__LOGIN=request.session['lid'])
    return render(request,"restaurant/view_menu.html",{"data":data})

def edit_menu(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "EDIT MENU"
    data = menu.objects.get(id=id)
    return render(request,"restaurant/edit_menu.html",{"data":data,"id":id})

def edit_menu_post(request,id):
    try:
        name = request.POST['textfield']
        amount = request.POST['textfield2']
        image = request.FILES['fileField']
        fs = FileSystemStorage()
        dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fs.save(r"C:\Users\DELL\PycharmProjects\RestaurantApp\myapp\static\menu\\" + dt + '.jpg', image)
        path = '/static/menu/' + dt + '.jpg'
        menu.objects.filter(id=id).update(name = name,amount = amount,photo = path,RESTAURANT = restaurant.objects.get(LOGIN=request.session['lid']))
        return HttpResponse("<script>alert('Updated!');window.location='/view_menu'</script>")
    except Exception as e:
        name = request.POST['textfield']
        amount = request.POST['textfield2']
        menu.objects.filter(id=id).update(name=name, amount=amount,
                                          RESTAURANT=restaurant.objects.get(LOGIN=request.session['lid']))
        return HttpResponse("<script>alert('Updated!');window.location='/view_menu'</script>")

def remove_menu(request,id):
    menu.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Removed!');window.location='/view_menu'</script>")

# ========== DELIVERY BOY MANAGEMENT ================

def add_delivery_boy(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "ADD DELIVERY BOY"
    return render(request,"restaurant/add_delivery_boy.html")

def add_delivery_boy_post(request):
    name = request.POST['textfield']
    contact = request.POST['textfield2']
    vehical_info = request.POST['textfield3']
    latitude = request.POST['textfield8']
    longitude = request.POST['textfield9']
    data = delivery_boy.objects.filter(name=name,contact=contact,vehical_info=vehical_info)
    if data.exists():
        return HttpResponse("<script>alert('Already exists!');window.location='/add_delivery_boy'</script>")
    else:
        obj = delivery_boy()
        obj.name = name
        obj.contact = contact
        obj.vehical_info = vehical_info
        obj.latitude = latitude
        obj.longitude = longitude
        obj.RESTAURANT = restaurant.objects.get(LOGIN=request.session['lid'])
        obj.save()
        return HttpResponse("<script>alert('Success!');window.location='/add_delivery_boy'</script>")

def view_delivery_boy(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW DELIVERY BOY"
    data = delivery_boy.objects.filter(RESTAURANT__LOGIN=request.session['lid'])
    return render(request,"restaurant/view_delivery_boy.html",{"data":data})

def update_delivery_boy(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "UPDATE BOY"
    data = delivery_boy.objects.get(id=id)
    return render(request,"restaurant/edit_delivery_boy.html",{"data":data,"id":id})

def update_delivery_boy_post(request,id):
    name = request.POST['textfield']
    contact = request.POST['textfield2']
    vehical_info = request.POST['textfield3']
    latitude = request.POST['textfield8']
    longitude = request.POST['textfield9']
    delivery_boy.objects.filter(id=id).update(name = name,contact = contact,vehical_info = vehical_info,latitude = latitude,longitude = longitude)
    return HttpResponse("<script>alert('Updated!');window.location='/view_delivery_boy'</script>")

def delete_delivery_boy(request,id):
    delivery_boy.objects.get(id=id).delete()
    return HttpResponse("<script>alert('Removed!');window.location='/view_delivery_boy'</script>")

def restaurant_view_order(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW ORDER"
    data = orderr.objects.filter(RESTAURANT__LOGIN=request.session['lid'])
    return render(request,"restaurant/view_order.html",{"data":data})

def allocate_delivery_boy(request,id):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "ALLOCATE DELIVERY BOY"
    data = delivery_boy.objects.all()
    return render(request,"restaurant/allocate_delivery_boy.html",{"data":data,"id":id})

def allocate_delivery_boy_post(request,id):
    delivery_boy_name = request.POST['select']
    obj = allocate()
    obj.DELIVERY_BOY_id = delivery_boy_name
    obj.ORDER_id = id
    obj.save()
    return HttpResponse("<script>alert('Allocated!');window.location='/restaurant_view_order'</script>")

def restaurant_view_rating(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW RATING"
    res = rating_and_comment.objects.filter(RESTAURANT__LOGIN=request.session['lid'])
    fs = "/static/star/full.jpg"
    hs = "/static/star/half.jpg"
    es = "/static/star/empty.jpg"
    data = []

    for rt in res:
        a = float(rt.rating)

        if a >= 0.0 and a < 0.4:
            ar = [es, es, es, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )

        elif a >= 0.4 and a < 0.8:
            ar = [hs, es, es, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 0.8 and a < 1.4:
            ar = [fs, es, es, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 1.4 and a < 1.8:
            ar = [fs, hs, es, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 1.8 and a < 2.4:
            ar = [fs, fs, es, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 2.4 and a < 2.8:
            ar = [fs, fs, hs, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 2.8 and a < 3.4:
            ar = [fs, fs, fs, es, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 3.4 and a < 3.8:
            ar = [fs, fs, fs, hs, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 3.8 and a < 4.4:
            ar = [fs, fs, fs, fs, es]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 4.4 and a < 4.8:
            ar = [fs, fs, fs, fs, hs]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )


        elif a >= 4.8 and a <= 5.0:
            ar = [fs, fs, fs, fs, fs]
            data.append(
                {
                    "rating": ar,
                    "review": rt.review,
                    "USER": rt.USER,
                    "RESTAURANT": rt.RESTAURANT,
                    "date": rt.date

                }
            )
    return render(request,"restaurant/view_rating.html",{"data":data})

def restaurant_change_password(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "CHANGE PASSWORD"
    return render(request,"restaurant/change_password.html")

def restaurant_change_password_post(request):
    old = request.POST['textfield']
    new = request.POST['textfield2']
    confirm = request.POST['textfield3']
    res = login.objects.filter(password=old,id=request.session['lid'])
    if res.exists():
        if new == confirm:
            login.objects.filter(id=request.session['lid']).update(password=confirm)
            return HttpResponse("<script>alert('Password updated');window.location='/restaurant_change_password'</script>")
        else:
            return HttpResponse("<script>alert('Password mismatch');window.location='/restaurant_change_password'</script>")
    else:
        return HttpResponse("<script>alert('Doesnt Exists!! ');window.location='/restaurant_change_password'</script>")


# =========== (PAYMENT HISTORY) =====================

def restaurant_view_payment(request):
    if "lid" not in request.session:
        return HttpResponse("<script>alert('Session Expired!Please Login Again');window.location='/'</script>")
    request.session['head'] = "VIEW PAYMENT HISTORY"
    return render(request,"restaurant/view_payment_history.html")

def restaurant_view_payment_post(request):
    month = request.POST['select']
    year = request.POST['select2']

    month_mapping = {
        "January": "01", "Februvary": "02", "March": "03", "April": "04",
        "May": "05", "June": "06", "July": "07", "August": "08",
        "september": "09", "october": "10", "november": "11", "december": "12"
    }

    month_number = month_mapping.get(month, "00")
    formatted_date = f"{year}-{month_number}"
    res = order_sub.objects.filter(ORDER__payment_date__startswith=formatted_date).aggregate(
        total_amount=Sum('ORDER__amount'))
    data = [{
        "total_amount": res.get('total_amount') or 0
    }]

    return render(request, "restaurant/view_payment_history.html", {"data": data})






#======================== USER MODULE ============================================(ANDROID)

def and_login(request):
    name = request.POST['name']
    password = request.POST['password']
    data = login.objects.filter(username=name,password=password)
    if data.exists():
        lid = data[0].id
        type = data[0].usertype
        return JsonResponse({"status":"ok","lid":lid,"type":type})
    else:
        return JsonResponse({"status":None})

def and_user_register(request):
    name = request.POST['name']
    email = request.POST['email']
    contact = request.POST['contact']
    place = request.POST['place']
    post = request.POST['post']
    pin = request.POST['pin']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    password = request.POST['password']
    image = request.FILES['pic']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\DELL\PycharmProjects\RestaurantApp\myapp\static\user_profile\\" + dt + '.jpg', image)
    path = '/static/user_profile/' + dt + '.jpg'
    res = login.objects.filter(username=email)
    if res.exists():
        return JsonResponse({"status":None})
    else:
        obj = login()
        obj.username = email
        obj.password = password
        obj.usertype = 'user'
        obj.save()
        obj1 = user()
        obj1.name = name
        obj1.email = email
        obj1.contact = contact
        obj1.place = place
        obj1.post = post
        obj1.pin = pin
        obj1.latitude = latitude
        obj1.longitude = longitude
        obj1.image = path
        obj1.LOGIN = obj
        obj1.save()
        return JsonResponse({"status":"ok"})

def and_view_nearby_restaurant(request):
    qry = restaurant.objects.filter(LOGIN__usertype='restaurant')
    lati = request.POST['lati']
    longi = request.POST['longi']
    latitude = str(lati)
    longitude = str(longi)

    ###### NEAR-BY code

    gcd_formula = "6371 * acos(least(greatest(cos(radians(%s)) * cos(radians('" + latitude + "')) * cos(radians('" + longitude + "') - radians(%s)) + sin(radians(%s)) * sin(radians('" + latitude + "')), -1), 1))"
    ar = []
    for i in qry:
        qs = restaurant.objects.filter(id=i.id).annotate(distance=RawSQL(gcd_formula, (i.latitude, i.longitude, i.latitude))).order_by('distance')
        ar.append({
            "rid": i.id,
            "name": i.name,
            "email":i.email,
            "contact":i.contact,
            "latitude":i.latitude,
            "longitude":i.longitude,
            "restaurant_distance":qs[0].distance
        })

    #### Distance arranging.........................

    def restaurant_nearby_sort(e):
        return e['restaurant_distance']

    ar.sort(key=restaurant_nearby_sort)


    return JsonResponse({"status":"ok","data":ar})


def and_change_password(request):
    old = request.POST['old']
    new = request.POST['new']
    confirm = request.POST['confirm']
    lid = request.POST['lid']
    data =login.objects.filter(password=old,id=lid)
    if data.exists():
        if new==confirm:
            login.objects.filter(id=lid).update(password=confirm)
            return JsonResponse({"status":"ok"})
        else:
            return JsonResponse({"status":"no"})
    else:
        return JsonResponse({"status":None})


def and_send_feedback(request):
    feedbacks = request.POST['feedback']
    lid = request.POST['lid']
    obj = feedback()
    obj.feedbacks = feedbacks
    obj.date = datetime.datetime.now().date()
    obj.USER = user.objects.get(LOGIN=lid)
    obj.save()
    return JsonResponse({"status":"ok"})

def and_view_rating_and_comment(request):
    rid = request.POST['rid']
    res = rating_and_comment.objects.filter(RESTAURANT_id=rid)
    ar = []
    for i in res:
        ar.append(
            {
                "rating_id":i.id,
                "rating":i.rating,
                "comment":i.review,
                "date":i.date,
                "userinfo":i.USER.name
            }
        )
    return JsonResponse({"status":"ok","data":ar})

def and_view_menu(request):
    rid = request.POST['rid']
    res = menu.objects.filter(RESTAURANT_id=rid)
    ar = []
    for i in res:
        ar.append(
            {
                "mid":i.id,
                "name":i.name,
                "amount":i.amount,
                "image":i.photo,

            }
        )
    return JsonResponse({"status":"ok","data":ar})

# ===================== CART ==========================

def and_add_to_cart(request):
    menu_id = request.POST['mid']
    lid = request.POST['lid']
    qnty = request.POST['quantity']
    res = cart.objects.filter(USER__LOGIN=lid,MENU=menu_id)
    if res.exists():
        cart.objects.filter(id=res[0]).update(quantity=res[0].quantity + int(qnty))
        return JsonResponse({"status":"no"})
    else:
        obj = cart()
        obj.USER = user.objects.get(LOGIN=lid)
        obj.MENU_id = menu_id
        obj.quantity = qnty
        obj.save()
        return JsonResponse({"status":"ok"})

def and_view_cart(request):
    lid = request.POST['lid']
    res = cart.objects.filter(USER__LOGIN=lid)
    ar = []
    amount = 0
    t = 0
    for i in res:
        amount = int(i.quantity) * int(i.MENU.amount)
        t = int(t) + int(amount)
        ar.append(
            {
                "cart_id":i.id,
                "quantity":i.quantity,
                "username":i.USER.name,
                "contact":i.USER.contact,
                "menu_name":i.MENU.name,
                "menu_amount":i.MENU.amount,
                "menu_image":i.MENU.photo,
                "res_name":i.MENU.RESTAURANT.name,
                "res_contact":i.MENU.RESTAURANT.contact
            }
        )
    return JsonResponse({"status":"ok","data":ar,"amount":amount,"t":t})

def and_place_order(request):
    lid = request.POST['lid']
    type = request.POST['type']

    method = request.POST['method']
    data = cart.objects.filter(USER__LOGIN=lid)
    if data.exists():
        for res in data:
            resto_exist = orderr.objects.filter(RESTAURANT=res.MENU.RESTAURANT,USER=res.USER)
            if resto_exist.exists():

                currentamount = int(resto_exist[0].amount)
                total = currentamount + int(res.quantity) * int(res.MENU.amount)
                resto_exist.update(amount=total)

                obj2 = order_sub()
                obj2.quantity = res.quantity
                obj2.ORDER_id = resto_exist[0].id
                obj2.MENU = res.MENU
                obj2.save()
            else:

                if type == 'pre-booking':
                    date = request.POST['date']
                    obj1 = orderr()
                    obj1.date = datetime.datetime.now().date()
                    obj1.amount =int(res.quantity)*int(res.MENU.amount)
                    obj1.status = type
                    obj1.payment_date = date
                    obj1.payment_status = method
                    obj1.delivery_status = 'delivered'
                    obj1.USER = user.objects.get(LOGIN=lid)
                    obj1.RESTAURANT = res.MENU.RESTAURANT
                    obj1.save()

                    obj2 = order_sub()
                    obj2.quantity = res.quantity
                    obj2.ORDER = obj1
                    obj2.MENU = res.MENU
                    obj2.save()
                else:
                    obj1 = orderr()
                    obj1.date = datetime.datetime.now().date()
                    obj1.amount = int(res.quantity) * int(res.MENU.amount)
                    obj1.status = type
                    obj1.payment_date = datetime.datetime.now().date()
                    obj1.payment_status = method
                    obj1.delivery_status = 'delivered'
                    obj1.USER = user.objects.get(LOGIN=lid)
                    obj1.RESTAURANT = res.MENU.RESTAURANT
                    obj1.save()

                    obj2 = order_sub()
                    obj2.quantity = res.quantity
                    obj2.ORDER = obj1
                    obj2.MENU = res.MENU
                    obj2.save()

    cart.objects.filter(USER__LOGIN=lid).delete()
    return JsonResponse({"status":"ok"})

def and_cancel_cart(request):
    cart_id = request.POST['cart_id']
    cart.objects.get(id=cart_id).delete()
    return JsonResponse({"status":"ok"})


def and_view_order(request):
    lid = request.POST['lid']
    res = orderr.objects.filter(USER__LOGIN=lid)
    ar = []
    for i in res:
        ar.append(
            {
                "order_id":i.id,
                "amount":i.amount,
                "date":i.date,
                "status":i.status,
                "delivery_status":i.delivery_status,
                "payment_status":i.payment_status,
                "payment_date":i.payment_date,
                "res_name":i.RESTAURANT.name,
                "res_contact":i.RESTAURANT.contact
            }
        )
    return JsonResponse({"status":"ok","data":ar})

def and_sendrating_and_comment(request):
    rating = request.POST['rating']
    comment = request.POST['comment']
    lid = request.POST['lid']
    order_id = request.POST['order_id']
    res = order_sub.objects.filter(ORDER_id=order_id)
    for i in res:
        res_id = i.MENU.RESTAURANT_id
        obj = rating_and_comment()
        obj.rating  = rating
        obj.review = comment
        obj.USER = user.objects.get(LOGIN=lid)
        obj.date = datetime.datetime.now().date()
        obj.RESTAURANT_id = res_id
        obj.save()
        return JsonResponse({"status":"ok"})

    return JsonResponse({"status":None})


# ================ Group creation ===================

def and_add_group(request):
    grp_name = request.POST['group_name']
    pic = request.FILES['pic']
    fs = FileSystemStorage()
    dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    fs.save(r"C:\Users\DELL\PycharmProjects\RestaurantApp\myapp\static\group_icon\\" + dt + '.jpg', pic)
    path = '/static/group_icon/' + dt + '.jpg'
    lid = request.POST['lid']
    user_instance = user.objects.get(LOGIN=lid)

    obj = groups()
    obj.name = grp_name
    obj.USER = user_instance
    obj.icon = path
    obj.save()

    obj1 = group_member()
    obj1.GROUPS = obj
    obj1.USER = user.objects.get(LOGIN=lid)
    obj1.status = 'admin'
    obj1.save()

    return JsonResponse({"status":"ok"})

def and_view_group(request):
    res = group_member.objects.filter(USER__LOGIN=request.POST['lid'])
    ar = []
    for i in res:
        ar.append(
            {
                "group_id":i.GROUPS.id,
                "group_name":i.GROUPS.name,
                "user_name":i.GROUPS.USER.name,
                "user_contact":i.GROUPS.USER.contact,
                "image":i.GROUPS.icon,
                "permission":i.status,
            }
        )
    return JsonResponse({"status":"ok","data":ar})

def and_edit_groups(request):
    group_id = request.POST['group_id']
    res = groups.objects.get(id=group_id)
    return JsonResponse({"status":"ok","name":res.name,"photo":res.icon})

def and_edit_group(request):
    try:
        grp_name = request.POST['group_name']
        pic = request.FILES['pic']
        group_id = request.POST['group_id']
        fs = FileSystemStorage()
        dt = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        fs.save(r"C:\Users\DELL\PycharmProjects\RestaurantApp\myapp\static\group_icon\\" + dt + '.jpg', pic)
        path = '/static/group_icon/' + dt + '.jpg'
        groups.objects.filter(id=group_id).update(name = grp_name,icon = path)
        return JsonResponse({"status":"ok"})
    except Exception as e:
        grp_name = request.POST['group_name']
        group_id = request.POST['group_id']
        groups.objects.filter(id=group_id).update(name=grp_name)
        return JsonResponse({"status": "ok"})



def and_remove_grp(request):
    group_id = request.POST['group_id']
    groups.objects.get(id=group_id).delete()
    return JsonResponse({"status":"ok"})

def and_add_other_members(request):
    try:
        member_id = request.POST['member_id']
        group_id = request.POST['group_id']
        obj = group_member()
        obj.GROUPS_id = group_id
        obj.USER_id = member_id
        obj.status = 'member'
        obj.save()

        return JsonResponse({"status": "ok"})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})




def and_view_other_member(request):
    group_id = request.POST['group_id']
    lid = request.POST['lid']
    group_members_ids = group_member.objects.filter(GROUPS__id=group_id).values_list('USER__id', flat=True)
    res = user.objects.exclude(id__in=group_members_ids).exclude(LOGIN=lid)
    ar = []
    for i in res:
        ar.append(
            {
                "member_id":i.id,
                "name":i.name,
                "contact":i.contact
            }
        )
    return JsonResponse({"status":"ok","data":ar})

def and_view_member(request):
    group_id = request.POST['group_id']
    res = group_member.objects.filter(GROUPS_id=group_id)
    ar = []
    for i in res:
        ar.append(
            {
                "member_id":i.id,
                "name":i.USER.name,
                "contact":i.USER.contact,
                "status":i.status,
                "user_image":i.USER.image
            }
        )
    return JsonResponse({"status":"ok","data":ar})


def and_remove_member(request):
    member_id = request.POST['member_id']
    group_member.objects.get(id=member_id).delete()
    return JsonResponse({"status":"ok"})


# ================== RESTAURANT INFORMATION ============


def and_view_sharing_information(request):
    rid = request.POST.get('rid', '')
    lid = request.POST.get('lid', '')


    res = group_member.objects.filter(Q(status='admin') | Q(status='member'), USER__LOGIN=lid)


    group_data = []


    for member in res:
        othermember = group_member.objects.filter(~Q(id = member.id),GROUPS_id=member.GROUPS.id)
        om = []
        for i  in othermember:
            om.append(i.USER.name)
        om.append("You")
        group_data.append({
            "sid": member.id,
            "user_name": ','.join(om),
            "group_icon": member.GROUPS.icon,
            "group_name": member.GROUPS.name
        })

    return JsonResponse({"status": "ok", "data": group_data})

def and_add_information_details(request):
    sid = request.POST['sid']
    rid = request.POST['rid']
    sid = sid.split(',')


    for i in sid:
        try:
            obj = share()
            obj.GROUP_MEMBER_id = i
            obj.RESTAURANT_id = rid
            obj.date = datetime.datetime.now().date()
            obj.type = 'share'
            obj.message = ""
            obj.save()
        except:
            pass
    return JsonResponse({"status":"ok"})

def and_add_message(request):
    lid = request.POST['lid']
    group_id = request.POST['group_id']
    message = request.POST['message']
    obj = share()
    obj.GROUP_MEMBER_id = group_member.objects.get(USER__LOGIN=lid,GROUPS_id=group_id).id
    obj.RESTAURANT_id = restaurant.objects.filter()[0].id
    obj.type = 'message'
    obj.message = message
    obj.date = datetime.datetime.now().date()
    obj.save()
    return JsonResponse({"status":"ok"})


def and_view_message(request):
    group_id = request.POST['group_id']
    lid = request.POST['lid']
    res = share.objects.filter(GROUP_MEMBER__GROUPS_id= group_id).order_by('id')
    ar = []
    for i in res:
        user_id = i.GROUP_MEMBER.USER.LOGIN_id
        if str(user_id) == str(lid):
            if i.type == 'message':
                # print("ID" , i.id , "Message" , i.message)
                ar.append(
                    {
                        "message_id":i.id,
                        "username":i.GROUP_MEMBER.USER.name,
                        "restaurant_name":'',
                        "image":'no',
                        "message":i.message,
                        "type":"sent"
                    }
                )

            else:
                # print("ID", i.id, "Message", i.message)

                ar.append(
                    {
                        "message_id": i.id,
                        "username": i.GROUP_MEMBER.USER.name,
                        "message": i.RESTAURANT.name,
                        "restaurant_name": '',
                        "image":i.RESTAURANT.image,
                        "type": "sent"
                    }
                )
        else:
            # print("ID", i.id, "Message", i.message)

            if i.type == 'message':


                ar.append(
                    {
                        "message_id":i.id,
                        "username":i.GROUP_MEMBER.USER.name,
                        "restaurant_name":'',
                        "image":'no',
                        "message": i.message,
                        "type":"receive"
                    }
                )

            else:
                # print("ID", i.id, "Message", i.message)

                ar.append(
                    {
                        "message_id": i.id,
                        "username": i.GROUP_MEMBER.USER.name,
                        "restaurant_name": '',
                        "message": i.RESTAURANT.name,
                        "image":i.RESTAURANT.image,
                        "type": "receive"
                    }
                )
    return JsonResponse({"status":"ok","data":ar})





