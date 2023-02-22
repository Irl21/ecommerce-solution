from django.shortcuts import render
from django.views import generic
from .models import Product, OrderItem, Address
from .utils import get_or_set_order_session
from django.shortcuts import reverse, get_object_or_404, redirect
from .forms import AddToCartForm, CheckoutViewForm
from django.contrib import messages

# Create your views here.

class ProductView(generic.ListView):
    template_name = 'cart/product_list.html'
    queryset = Product.objects.all()

class ProductDetailView(generic.FormView):
    template_name = 'cart/product-detail.html'
    form_class = AddToCartForm
    

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs["slug"])

    def get_success_url(self):
        return reverse("home")
    def get_form_kwargs(self):
        kwargs = super(ProductDetailView, self).get_form_kwargs()
        kwargs['product_id'] = self.get_object().id
        return kwargs
    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        product = self.get_object()
        

        item_filter = order.items.filter(product=product,
                color = form.cleaned_data['color'],
                size = form.cleaned_data['size']
                
                )

        if item_filter.exists():
            item = item_filter.first()
            item.quantity += int(form.cleaned_data['quantity'])
            item.save()
        else:
            new_item = form.save(commit=False)
            new_item.product = product
            new_item.order = order
            new_item.save()
        return super(ProductDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.get_object()

        return context


class CartView(generic.TemplateView):
    template_name = 'cart/cart.html'
    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)

        return context

class IncreaseQuantityView(generic.View):

    def  get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.quantity+=1
        order_item.save()

        return redirect("cart:summary")

class DecreaseQuantityView(generic.View):
    def  get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
    

        if order_item.quantity <= 1:
            order_item.delete()
        else:
            order_item.quantity-=1
            order_item.save()

        return redirect("cart:summary")

class RemoveItemView(generic.View):
    def  get(self, request, *args, **kwargs):
        order_item = get_object_or_404(OrderItem, id=kwargs['pk'])
        order_item.delete()

        return redirect("cart:summary")

class CheckoutView(generic.FormView):
    template_name = 'cart/checkout.html'
    form_class = CheckoutViewForm

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['order'] = get_or_set_order_session(self.request)

        return context

    def get_form_kwargs(self):
        kwargs = super(CheckoutView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        order = get_or_set_order_session(self.request)
        selected_billing_address = form.cleaned_data.get('selected_billing_address')
        selected_shipping_address = form.cleaned_data.get('selected_shipping_address')

        if selected_billing_address:
            order.billing_address = selected_billing_address
        else:
            address = Address.objects.create(
                user=self.request.user,
                county = form.cleaned_data.get('billing_county'),
                postal_code = form.cleaned_data.get('billing_postal_code'),
                phone_number1 = form.cleaned_data.get('billing_phone_number1'),
                phone_number2 = form.cleaned_data.get('billing_phone_number2'),
                Address_type = form.cleaned_data.get('B')
            )
            order.billing_address = address
        order.save()

        if selected_shipping_address:
            order.shipping_address = selected_shipping_address
        else:
            address = Address.objects.create(
                user=self.request.user,
                county = form.cleaned_data.get('shipping_county'),
                postal_code = form.cleaned_data.get('shipping_postal_code'),
                phone_number1 = form.cleaned_data.get('shipping_phone_number1'),
                phone_number2 = form.cleaned_data.get('shipping_phone_number2'),
                Address_type = form.cleaned_data.get('S')
            )

            order.shipping_address = address
        order.save()

        messages.success(self.request, 'You have succesfully added your addresses')

        

        return super(CheckoutView, self).form_valid(form)



