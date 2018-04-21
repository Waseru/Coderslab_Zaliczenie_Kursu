"""FINAL_PROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from orders.views import ProductView, LoginView, AddUserView, OrdersView, LogoutView, CreateOrderView, OrderDetailView, \
    CreateOrderView2

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^products/$', ProductView.as_view(), name='products'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^create_user/$', AddUserView.as_view(), name='create_user'),
    url(r'^orders_view/$', OrdersView.as_view(), name='orders-view'),
    url(r'^order_detail_view/(?P<id>\d+)/$', OrderDetailView.as_view(), name='detail-view'),
    url(r'^create_order/$', CreateOrderView.as_view()),
    url(r'^create_order2/$', CreateOrderView2.as_view()),
]
