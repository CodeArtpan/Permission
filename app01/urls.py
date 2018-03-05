from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^index$',views.index),

    url(r'^users$',views.users),
    url(r'^user/add$',views.useradd),
    url(r'^user/edit/(\d+)$',views.useredit),
    url(r'^user/del/(\d+)$',views.userdel),

    url(r'^orders$', views.orders),
    url(r'^order/add$', views.orderadd),
    url(r'^order/edit/(\d+)$', views.orderedit),
    url(r'^order/del/(\d+)$', views.orderdel),

]
