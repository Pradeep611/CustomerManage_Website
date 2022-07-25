from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *  # this will import all the models from models.py
from .forms import OrderForm,CreateUserForm #this will OrderForm model from forms.py
from django.forms import inlineformset_factory
from .filter import FilterForm
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def RegisterPage(request):
    form = CreateUserForm()
    

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
           form.save()
           print("user created")
    print("user creation failed")

    context = {'form':form}
    return render(request,'accounts/register.html',context)

def LoginPage(request):
    return render(request,'accounts/login.html')

def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()
    orders_delivered = orders.filter(status = 'Delivered').count()
    orders_pending = orders.filter(status = 'Pending').count()

    context = {'customers':customers,'orders':orders,'total_orders':total_orders,'orders_delivered':orders_delivered,'orders_pending':orders_pending}

    return render(request,'accounts/dashboard.html',context)

def products(request):
    products = Product.objects.all()

    return render(request,'accounts/products.html',{'products':products})

def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    filter = FilterForm(request.GET,queryset=orders)
    orders = filter.qs


    context = {'customer':customer,'orders':orders,'order_count':order_count,'filter':filter}
    return render(request,'accounts/customer.html',context)


def create_order(request,pk):
    customer = Customer.objects.get(id = pk)
   
   # form = OrderForm(initial = {'customer':customer}) # this will get all the fields dynamic data of the Order Model 
    OrderFormSet = inlineformset_factory(Customer,Order,fields = ('product','status'),extra = 10)

    formset = OrderFormSet(queryset = Order.objects.none(),instance = customer)


    if request.method == 'POST':
        #print('printing post:',request.POST)
        #form = OrderForm(request.POST) #here forms is giving all the data that we have filled on create_order url page
        
        formset = OrderFormSet(request.POST,instance = customer)
        if formset.is_valid():
            formset.save()     #b/c of this forms.save() only the data is being saved and visible on 
            return redirect('/') #using this we will directly redirect to home page after submitting data


    context = {'formset':formset}
    return render(request,'accounts/order_form.html',context)

def update_order(request,pk):
    

    order = Order.objects.get(id=pk) #this will give us the information of order object belong to id=pk
    form = OrderForm(instance = order)
    
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order) #request.post will post the data that we will update if you dont use request.post data won't be changed and instance=order will only give us the form for order at that instance
        if form.is_valid():
            form.save()    #if u don't save the form,it will be not be updated after changes
            return redirect('/')

    context = {'form':form}
    return render(request,'accounts/order_form.html',context)

def delete_order(request,pk):
    order = Order.objects.get(id=pk)
    # form = OrderForm(instance = order)

    if request.method == 'POST':
        order.delete()
        print("hii, you were right")
        return redirect('/')
      
    context = {'item':order}
    return render(request,'accounts/delete.html',context)


