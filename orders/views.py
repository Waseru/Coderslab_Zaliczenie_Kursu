from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from orders.forms import LoginForm, AddUserForm, OrderProductForm
from orders.models import Product, ProductPart, Order, OrderData


# Create your views here.

class ProductView(View):
    def get(self, request):
        products = Product.objects.all()
        productpart = ProductPart.objects.all()
        ctx = {
            "products": products,
            "productpart": productpart
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
                # ----------------------- dzien 3 uprawnienia --------
                url = request.GET.get('next')
                if url:
                    return redirect(url)
                # sprawia, że jesli np. nie jestem zalogowany, a chce zmienic hasło, to mnie przekierowuje do strony z logowaniem
                # do formularza z logowaniem
                # ------------------------------------------------------
                order_list = Order.objects.filter(user=request.user)

                ctx = {
                    "order_list": order_list,
                }
                return render(request, 'orders_view.html', ctx)
            # else:
            #     return HttpResponse('Zły login lub hasło')
            form.add_error(field=None, error='Zły login lub hasło') #zamiennie moze byc
        ctx = {
            'form': form,
        }
        return render(request, 'products.html', ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'products.html')

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
            return HttpResponse('Utworzono uzytkownika o id {}'.format(user.id))
        ctx = {
            'form': form,
        }
        return render(request, 'login_form.html', ctx)


class CreateOrderView(View):
    def get(self, request):
        form = formset_factory(OrderProductForm, extra=2)()
        ctx = {
            'form': form,
        }
        return render(request, 'order_form.html', ctx)

    def post(self, request):
        form = formset_factory(OrderProductForm, extra=2)(request.POST)
        if form.is_valid():
            object = Order.objects.create(user=request.user)
            # products = form.cleaned_data['product']
            for product in form.cleaned_data:
                quantity = product.get('quantity')
                name = product.get('product')
                stocks = ProductPart.objects.filter(product_name=name).exclude(quantity=0).order_by('-expire_date')
                if not stocks:
                    #usunąć stworzony obiekt
                    return HttpResponse('Przepraszamy! Produkt {} jest niedostępny'.format(name))
                else:
                    for stock in stocks:
                        if stock.quantity > quantity:
                            stock.quantity -= quantity
                            stock.save()
                            order = OrderData(product=name, product_part=stock, order=object, order_quantity=quantity)
                            order.save()
            return render(request, 'order_form.html', )



                #do sprawdzenia czy quantity jest odpowiednie trzeba chyba petle for zrobić z ifem w środku do zapisu danych
            #     order = OrderData(product=name, product_part=stock, order=object, order_quantity=quantity)
            #     order.save()
            #     # stock.quantity -= quantity
            #     # stock.save()
            #     # return HttpResponse(stock.quantity)
            # return HttpResponse(order)

class CreateOrderView2(View):
    def get(self, request):
        form = BiggerOrderDataForm
        ctx = {
            'form': form,
        }
        return render(request, 'create_order_form.html', ctx)

class OrdersView(View):
    def get(self, request):
        order_list = Order.objects.filter(user=request.user)

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

