from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from orders.forms import LoginForm, AddUserForm
from orders.models import Product

# Create your views here.

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
                # ----------------------- dzien 3 uprawnienia --------
                url = request.GET.get('next')
                if url:
                    return redirect(url)
                # sprawia, że jesli np. nie jestem zalogowany, a chce zmienic hasło, to mnie przekierowuje do strony z logowaniem
                # do formularza z logowaniem
                # ------------------------------------------------------
                return HttpResponse('zostałeś zalogowany')
            # else:
            #     return HttpResponse('Zły login lub hasło')
            form.add_error(field=None, error='Zły login lub hasło') #zamiennie moze byc
        ctx = {
            'form': form,
        }
        return render(request, 'login_form.html', ctx)

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