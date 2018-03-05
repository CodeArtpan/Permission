from django.shortcuts import render,HttpResponse,redirect

def index(request):
    return render(request,'index.html')

def users(request):
    return HttpResponse('用户列表')

def useradd(request):
    return HttpResponse('增加用户')

def useredit(request,id):
    return HttpResponse('编辑用户')

def userdel(request,id):
    return HttpResponse('删除用户')

def orders(request):
    return HttpResponse('订单列表')

def orderadd(request):
    return HttpResponse('增加订单')

def orderedit(request,id):
    return HttpResponse('编辑订单')

def orderdel(request,id):
    return HttpResponse('删除订单')