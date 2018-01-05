#mapper for directing URLs to views

from django.conf.urls import url
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView


from . import views


urlpatterns = [
	path(r'', RedirectView.as_view(url='/market/portfolio/', permanent=True)),
	url(r'^stocks/$', views.StockListView.as_view(), name='stocks'),
	url(r'^stock/(?P<pk>[A-Z]+)$', views.StockDetailView.as_view(), name='stock-detail'),
	url(r'^portfolio/$', views.UserDetailView.as_view(), name='portfolio'),
	url(r'^stock/(?P<pk>[A-Z]+)/buy/$', views.buyStock, name='buy-stock'),
	url(r'^portfolio/deposit/$', views.depositCash, name='deposit-cash'),
	url(r'^portfolio/withdrawal/$', views.withdrawCash, name='withdraw-cash'),
	url(r'^holding/(?P<pk>.+)/sell/$', views.sellStock, name='sell-stock'),
]