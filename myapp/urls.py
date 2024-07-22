"""RestaurantApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.log),
    path('log_post',views.log_post),
    path('admin_home',views.admin_home),
    path('logout',views.logout),
    path('forgot_password',views.forgot_password),
    path('forgot_password_post',views.forgot_password_post),
    path('change_password',views.change_password),
    path('change_password_post',views.change_password_post),
    path('admin_view_restaurant',views.admin_view_restaurant),
    path('approve_restaurnant/<id>',views.approve_restaurnant),
    path('reject_restaurnant/<id>',views.reject_restaurnant),
    path('admin_view_verified_restaurant',views.admin_view_verified_restaurant),
    path('view_restaurant_rating/<id>',views.view_restaurant_rating),
    path('admin_view_delivery_boy/<id>',views.admin_view_delivery_boy),
    path('admin_view_user',views.admin_view_user),
    path('admin_view_feedback',views.admin_view_feedback),
    path('view_payment',views.view_payment),
    path('view_payment_post',views.view_payment_post),

#======================================================================================== RESTAURANT
    path('register',views.register),
    path('register_post',views.register_post),
    path('restaurant_home',views.restaurant_home),
    path('add_menu',views.add_menu),
    path('add_menu_post',views.add_menu_post),
    path('view_menu',views.view_menu),
    path('edit_menu/<id>',views.edit_menu),
    path('edit_menu_post/<id>',views.edit_menu_post),
    path('remove_menu/<id>',views.remove_menu),
    path('add_delivery_boy',views.add_delivery_boy),
    path('add_delivery_boy_post',views.add_delivery_boy_post),
    path('view_delivery_boy',views.view_delivery_boy),
    path('update_delivery_boy/<id>',views.update_delivery_boy),
    path('update_delivery_boy_post/<id>',views.update_delivery_boy_post),
    path('delete_delivery_boy/<id>',views.delete_delivery_boy),
    path('restaurant_view_order',views.restaurant_view_order),
    path('allocate_delivery_boy/<id>',views.allocate_delivery_boy),
    path('allocate_delivery_boy_post/<id>',views.allocate_delivery_boy_post),
    path('restaurant_view_rating',views.restaurant_view_rating),
    path('restaurant_change_password',views.restaurant_change_password),
    path('restaurant_change_password_post',views.restaurant_change_password_post),
    path('restaurant_view_payment',views.restaurant_view_payment),
    path('restaurant_view_payment_post',views.restaurant_view_payment_post),

#================================================================================================== USER
    path('and_login',views.and_login),
    path('and_user_register',views.and_user_register),
    path('and_view_nearby_restaurant',views.and_view_nearby_restaurant),
    path('and_change_password',views.and_change_password),
    path('and_send_feedback',views.and_send_feedback),
    path('and_sendrating_and_comment',views.and_sendrating_and_comment),
    path('and_view_rating_and_comment',views.and_view_rating_and_comment),
    path('and_view_menu',views.and_view_menu),
    path('and_add_to_cart',views.and_add_to_cart),
    path('and_view_cart',views.and_view_cart),
    path('and_cancel_cart',views.and_cancel_cart),
    path('and_place_order',views.and_place_order),
    path('and_view_order',views.and_view_order),
    path('and_add_group',views.and_add_group),
    path('and_view_group',views.and_view_group),
    path('and_edit_groups',views.and_edit_groups),
    path('and_edit_group',views.and_edit_group),
    path('and_remove_grp',views.and_remove_grp),
    path('and_add_other_members',views.and_add_other_members),
    path('and_view_other_member',views.and_view_other_member),
    path('and_view_member',views.and_view_member),
    path('and_remove_member',views.and_remove_member),
    path('and_view_sharing_information',views.and_view_sharing_information),
    path('and_add_information_details',views.and_add_information_details),
    path('and_view_message',views.and_view_message),
    path('and_add_message',views.and_add_message),



]
