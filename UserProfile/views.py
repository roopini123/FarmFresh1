from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .forms import UserEditForm, UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from base64 import b64decode
from django.core.files.base import ContentFile
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
import uuid
from django.contrib.auth import authenticate, login, logout
from shop.models import Product,Order
User = get_user_model()

# @login_required
# def index(request):
#    	return render(request,'index.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_first_time=False
            user.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect("/user/details/{0}".format(user.id))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'user/change_pwd.html',{ 'form': form })


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('/')

            # img=request.POST.get('picBs64')
            # header, data = img.split(",", 1)
            # image_data = b64decode(data)
            # user.picture = ContentFile(image_data, str(uuid.uuid4().hex.upper()[0:6])+'.png')

            # return HttpResponseRedirect('/login')

    else:
        form = UserRegisterForm()
    return render(request,'registration/register.html',{'form':form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(request.POST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

@login_required
def user_update(request,id=None):
    instance = get_object_or_404(User,id=id)
    form = UserEditForm(request.POST or None,request.FILES or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/user/details/{0}".format(instance.id))

    context ={
              'instance' : instance,
              'form':form ,
    }
    return  render (request,"user/edit.html" , context)

@login_required
def user_detail(request,id=None):
	instance = get_object_or_404(User,id=id)
	context ={
			'instance' : instance,
	}
	return  render (request,"user/details.html" , context)


@login_required
def my_orders(request):
    orders = Order.objects.filter(user_id=request.user.id)
    context ={
            'orders' : orders,
    }
    return  render (request,"user/myorders.html" , context)


