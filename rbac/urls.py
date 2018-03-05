from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^login/$',views.login),
    url(r'^users/$',views.users),
    url(r'^user/add/$',views.useradd),
    url(r'^user/edit/(\d+)/$',views.useredit),

]
