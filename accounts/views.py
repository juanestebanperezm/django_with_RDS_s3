from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from .models import *
from django.db.models import Count
from .forms import *
from django.forms import inlineformset_factory
from .filters import FilterOrder
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def settings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request,'settings.html',context)




#User page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()
    delivered=orders.filter(status='Entregado').count()
    pending=orders.filter(status='Pendiente').count()
    context={
    'orders':orders,
    'total_orders':total_orders,
    
    'delivered':delivered,
    'pending':pending}
    return render(request,'user_page.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('user-page')
        
        
        if user.is_staff:
            login(request,user)
            return redirect('home')
        
        else:
            messages.info(request,'Usuario o contraseña incorrecta')
    context={}
    return render(request,'login.html',context)


def Logoutuser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerPage(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            usuario=form.cleaned_data.get('username')

            
            
            messages.success(request,'La cuenta de '+usuario+' fue creada')
            return redirect('login')
    context={'form':form}
    return render(request,'register.html',context)


#######
@login_required(login_url='login')
@admin_only
def Home(request):
    clients=Customer.objects.all()
    orders=Order.objects.all()

    total_customers=clients.count()
    total_orders=orders.count()
    delivered=orders.filter(status='Entregado').count()
    pending=orders.filter(status='Pendiente').count()

    contexto={
    'clients':clients,
    'orders':orders,
    'total_orders':total_orders,
    'total_customers':total_customers,
    'delivered':delivered,
    'pending':pending
    }
    return render(request,'index.html',contexto)

    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Products(request):
    products=Product.objects.all()
    contexto={'products':products}
    return render(request,'products.html',contexto)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def Clientes(request,pk_test):
    clients=Customer.objects.get(id=pk_test)
    orders=clients.order_set.all()
    orders_count=orders.count()
    miFiltro=FilterOrder(request.GET,queryset=orders)
    orders=miFiltro.qs
    contexto={
        'clients':clients,
        'orders':orders,
        'orders_count':orders_count,
        'miFiltro':miFiltro
    
    }
    return render(request,'clientes.html',contexto)


#Create
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def CreateOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
    customer=Customer.objects.get(id=pk)
    formSet=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form=OrderForm(initial={'customer':customer})
    if request.method=='POST':
        formSet=OrderFormSet(request.POST,instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect('/')
    contexto={'formSet':formSet}
    return render(request,'order_form.html',contexto)

@login_required(login_url='login')

def CreateCustomer(request):
    form=CustomerForm()
    if request.method=='POST':
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    contexto={'form':form}
    return render(request,'customer_form.html',contexto)


#Update

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method=='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    contexto={'form':form}
    return render(request,'order_form.html',contexto)

@login_required(login_url='login')
def UpdateCustomer(request,pk):
    customer=Customer.objects.get(id=pk)
    form=CustomerForm(instance=customer)
    if request.method=='POST':
        form=CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    contexto={'form':form}
    return render(request,'customer_form.html',contexto)


#Delete
@login_required(login_url='login')
def DeleteCustomer(request,pk):
    customer=Customer.objects.get(id=pk)
    if request.method=='POST':
        customer.delete()
        return redirect('/')
    contexto={'customer':customer}
    return render(request,'delete_customer.html',contexto)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def DeleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('/')
    contexto={'order':order}

    return render(request,'delete_order.html',contexto)