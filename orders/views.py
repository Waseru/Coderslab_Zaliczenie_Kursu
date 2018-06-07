from datetime import timedelta, datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from orders.forms import LoginForm, AddUserForm, OrderProductForm
from orders.models import Product, ProductPart, Order, OrderData


class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        ctx = {
            "products": products,
        }
        return render(request, 'products.html', ctx)

class LoginView(View):
    def get(self, request):
        form = LoginForm
        ctx = {
            'form': form,
        }
        return render(request, 'login_form.html', ctx)


    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                url = request.GET.get('next')
                if url:
                    return redirect(url)

                products = Product.objects.all()

                ctx = {
                    "products": products,
                }
                return render(request, 'products.html', ctx)
            else:
                return HttpResponse('Zły login lub hasło')

        ctx = {
            'form': form,
        }
        return render(request, 'products.html', ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        products = Product.objects.all()
        ctx = {
            "products": products,
        }
        return render(request, 'products.html', ctx)

class AddUserView(View):
    def get(self, request):
        form = AddUserForm
        ctx = {
            'form': form
        }
        return render(request, 'login_form.html', ctx)

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            del form.cleaned_data['confirm_password']
            user = User.objects.create_user(**form.cleaned_data)
            user = authenticate(**form.cleaned_data)
            if user:
                login(request, user)
                url = request.GET.get('next')
                if url:
                    return redirect(url)
            products = Product.objects.all()
            ctx = {
                "products": products,
            }
            return render(request, 'products.html', ctx)
        ctx = {
            'form': form,
        }
        return render(request, 'login_form.html', ctx)


class CreateOrderView(View):
    def get(self, request):
        form = formset_factory(OrderProductForm, extra=3)()
        ctx = {
            'form': form,
        }
        return render(request, 'order_form.html', ctx)

    def post(self, request):
        form = formset_factory(OrderProductForm, extra=3)(request.POST)
        if form.is_valid():
            object = Order.objects.create(user=request.user)
            repetition = []
            for product in form.cleaned_data:
                repetition.append(product.get('product'))
                if repetition.count(product.get('product')) >= 2:
                    return HttpResponse('Podałeś  conajmniej dwa razy ten sam produkt! {}'.format(product.get('product')))

            for product in form.cleaned_data:
                quantity = product.get('quantity')
                name = product.get('product')
                stocks = ProductPart.objects.filter(product_name=name).exclude(quantity=0).order_by('-expire_date')
                if not stocks:
                    object.delete()
                    return HttpResponse('Przepraszamy! Produkt {} jest niedostępny'.format(name))
                else:
                    for stock in stocks:
                        if stock.quantity > quantity:
                            stock.quantity -= quantity
                            stock.save()
                            order = OrderData(product=name, product_part=stock, order=object, order_quantity=quantity)
                            order.save()
                            break
            ctx = {
                'form': form,
            }
            return render(request, 'order_form.html', ctx)


class OrdersView(View):
    def get(self, request):
        order_list = Order.objects.filter(user=request.user).order_by('-order_date')

        ctx = {
            "order_list": order_list,
        }
        return render(request, 'orders_view.html', ctx)

class OrderDetailView(View):
    def get(self, request, id):
        order_list = Order.objects.get(id=id)
        ctx = {
            "order_list": order_list,
        }
        return render(request, 'order_detail_view.html', ctx)

class UserExpireProductView(View):
    def get(self, request):
        orders_list = Order.objects.filter(user=request.user) #zamówienia danego użytkownika
        if not orders_list:
            return render(request, 'close_expire_list_no_orders.html')
        else:
            close_expire_date = datetime.now().date() + timedelta(days=7)
            date_now = datetime.now().date()

            list = []
            for order in orders_list:
                product_parts = OrderData.objects.filter(order=order) #dane obiektów do zamówień użytkownika
                for product_part in product_parts:
                    if date_now <= product_part.product_part.expire_date <= close_expire_date:
                        list.append(product_part.product_part)

                        ctx = {
                            'lists': list
                        }
            if not list:
                return render(request, 'close_expire_list_empty.html')
            else:
                return render(request, 'close_expire_list_form.html', ctx)
