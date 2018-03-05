from django.shortcuts import render,HttpResponse,redirect
from . import models
from rbac.service.initial import init_permission


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    user_obj = models.User.objects.filter(username=user,password=pwd).first()

    if not user_obj:
        error = '用户名或密码错误'
        return render(request,'login.html',{'error':error})

    init_permission(request,user_obj)

    return redirect('/app01/index')


#---------------------------------------use ModelForm CURD------------------------------------------------


from django.forms import ModelForm

class UserModelForm(ModelForm):
    class Meta:
        model = models.User
        fields = '__all__'

def users(request):
    user_list = models.User.objects.all()

    return render(request, 'users.html', {'user_list': user_list})

def useradd(request):
    if request.method == 'GET':
        modelform = UserModelForm()
    else:
        modelform = UserModelForm(request.POST)
        if modelform.is_valid():
            modelform.save()
            return redirect('/rbac/users/')
    return render(request,'useradd.html',{'modelform':modelform})


def useredit(request,pk):
    obj = models.User.objects.filter(pk=pk).first()
    if request.method == 'GET':
        modelform = UserModelForm(instance=obj)
    else:
        modelform = UserModelForm(request.POST,instance=obj)
        if modelform.is_valid():
            modelform.save()
            return redirect('/rbac/users/')
    return render(request, 'useredit.html', {'modelform': modelform})
