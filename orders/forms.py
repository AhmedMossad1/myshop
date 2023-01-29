#Present a user with an order form to fill in their data
from dataclasses import fields
from django import forms
from .models import Order

class OrderCreateForm (forms.ModelForm):
    class Meta :
        model = Order
        fields = ['first_name', 'last_name', 'email', 'addres',
                'postal_code', 'city']