from django import forms
from .models import OrderItem, ColorVariation, Product, SizeVariation, Address
from django.contrib.auth import get_user_model



User = get_user_model()

class AddToCartForm(forms.ModelForm):
    color = forms.ModelChoiceField(queryset=ColorVariation.objects.none())
    size = forms.ModelChoiceField(queryset=SizeVariation.objects.none())

    class Meta:
        model = OrderItem
        fields = ['quantity', 'color', 'size']

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id')
        product = Product.objects.get(id=product_id)
        super().__init__(*args, **kwargs)

        self.fields['color'].queryset=product.available_colours.all()
        self.fields['size'].queryset=product.available_sizes.all()

class CheckoutViewForm(forms.Form):
    billing_county = forms.CharField(required = False)
    billing_postal_code = forms.IntegerField(required = False)
    billing_phone_number1 = forms.IntegerField(required = False)
    billing_phone_number2 = forms.IntegerField(required = False)

    shipping_county = forms.CharField(required = False)
    shipping_postal_code = forms.IntegerField(required = False)
    shipping_phone_number1 = forms.IntegerField(required = False)
    shipping_phone_number2 = forms.IntegerField(required = False)

    selected_billing_address = forms.ModelChoiceField(queryset=Address.objects.none(), required = False)
    selected_shipping_address = forms.ModelChoiceField(queryset=Address.objects.none(), required = False)
    
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id')
        user = User.objects.get(id=user_id)
        super().__init__(*args, **kwargs)

        user = User.objects.get(id=user_id)

        billing_address_queryset = Address.objects.filter(
            user = user,
            Address_type = 'B'
        )
        shipping_address_queryset = Address.objects.filter(
            user = user,
            Address_type = 'S'
        )

        self.fields['selected_billing_address'].queryset= billing_address_queryset
        self.fields['selected_shipping_address'].queryset=shipping_address_queryset


    def clean(self):
        data = self.cleaned_data
        selected_billing_address = data.get('selected_billing_address', None)

        if selected_billing_address is None:
            if not data.get('billing_county', None):
                self.add_error('billing_county', 'this field must be filled')
            
            if not data.get('billing_postal_code', None):
                self.add_error('billing_postal_code', 'this field must be filled')
        
            if not data.get('billing_phone_number1', None):
                self.add_error('billing_phone_number1', 'this field must be filled')

            if not data.get('billing_phone_number2', None):
                self.add_error('billing_phone_number2', 'this field must be filled')

        selected_shipping_address = data.get('selected_shipping_address', None)
        if selected_shipping_address is None:
            if not data.get('shipping_county', None):
                self.add_error('shipping_county', 'this field must be filled')
            
            if not data.get('shipping_postal_code', None):
                self.add_error('shipping_postal_code', 'this field must be filled')
            
            if not data.get('shipping_phone_number1', None):
                self.add_error('shipping_phone_number1', 'this field must be filled')

            if not data.get('shipping_phone_number2', None):
                self.add_error('shipping_phone_number2', 'this field must be filled')

