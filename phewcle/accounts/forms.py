from django.forms import ModelForm  #ModelForm is a python way of creating forms
from .models import Order  #imported Order Model from models.py using this line
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order #this will tell us for which model we are building form
        fields = '__all__' #this will get all fields present in Order model in models.property

        # fields = ['products','customer'] #this will only get customer and product field from Order model

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']
