from django.shortcuts import render
from django.views import generic
from stockdata.stockdata import stockdata
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import datetime

from .forms import BuyStockForm
from .forms import SellStockForm
from .forms import DepositCashForm
from .forms import WithdrawCashForm
from .models import Stock, OwnedStock, User, Trader

from django.shortcuts import get_object_or_404


##################################### STANDARD VIEWS #####################################3

"""
View for generating a list of all the stocks available on the market and their prices
Uses the stockdata module for calling the AlphaVantage API
"""
class StockListView(generic.ListView):
	model = Stock
	paginate_by = 13
	template_name ='stock_list.html'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		symbols=Stock.objects.all().values('symbol')
		newList = list()
		for item in symbols:
			newList.append(item['symbol'])
		symbols = newList
		apiCaller = stockdata();
		prices = apiCaller.getQuotes(symbols);
		data['quotes'] = prices

		#gets the trader object associated with current user for displaying cash balances
		try:
			data['trader'] = Trader.objects.get(user=self.request.user)
		except:
			print("Not logged in")

		return data




"""
View for generating the detail about a stock
Uses the stockdata module for fetching the daily stock history
"""
class StockDetailView(generic.DetailView):
	model = Stock
	template_name ='stock_detail.html'
	#Get
	def get_object(self, queryset=Stock.objects.all()):
		stock = get_object_or_404(Stock, symbol__iexact=self.kwargs['pk'])
		return stock

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		apiCaller = stockdata();
		historic = apiCaller.getDaily(data['stock'])
		data['historic'] = historic
		data['price'] = historic[list(historic.keys())[0]]['close']

		#gets the trader object associated with current user for displaying cash balances
		try:
			data['trader'] = Trader.objects.get(user=self.request.user)
		except ObjectDoesNotExist:
			print("Not logged in")

		return data


"""
View for generating the users portfolio page which displays their holdings
"""
class UserDetailView(LoginRequiredMixin, generic.ListView):
	model = User
	template_name ='portfolio.html'

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		data['ownedstock_list'] = OwnedStock.objects.filter(owner=self.request.user).order_by('stock')
		currTrader = get_object_or_404(Trader, user=self.request.user)
		data['cash'] = currTrader.cash
		newList = list()

		#nFetching the stock symbols so we can get the latest price for each holding
		for item in data['ownedstock_list']:
			newList.append(str(item))
		symbols = newList
		apiCaller = stockdata();
		prices = apiCaller.getQuotes(symbols);
		data['quotes'] = prices

		#gets the trader object associated with current user for displaying cash balances
		try:
			data['trader'] = Trader.objects.get(user=self.request.user)
		except ObjectDoesNotExist:
			print("Not logged in")


		return data



######################################### FORMS ################################################

"""
Function for generating the form for purchasing stock
Validates the form and updates the users cash balance and portfolio
Note that this function DOES allow the user to get into negative balance
"""
@login_required(login_url='/accounts/login/')
def buyStock(request, pk):

	stock_inst=get_object_or_404(Stock, symbol__iexact=pk)

	apiCaller = stockdata();
	quote = apiCaller.getQuotes([stock_inst.symbol]);
	currTrader = get_object_or_404(Trader, user=request.user)
	cash = currTrader.cash


	if request.method == 'POST':
		form = BuyStockForm(request.POST)

		#if form is valid, then process the purchase
		if form.is_valid():

			purchased = OwnedStock(stock=stock_inst, 
									quantity=form.cleaned_data['quantity'], 
									price_at_purchase=quote[stock_inst.symbol]['price'], 
									owner=request.user,
									time_of_purchase=datetime.datetime.now())
			purchased.save()

			cost = form.cleaned_data['quantity']*float(quote[stock_inst.symbol]['price'])
			currTrader.cash -= cost
			currTrader.save()

			return HttpResponseRedirect(reverse('portfolio') )

	# If this is a GET (or any other method) create the default form.
	else:
		
		form = BuyStockForm()

	return render(request, 'buy_stock.html', 
		{'form': form, 
		'stockinst':stock_inst, 
		'quote':quote[stock_inst.symbol], 
		'cash':cash, 
		'trader':currTrader})


"""
Function for generating the view for selling stock
Uses the stockdata module to get the latest pricing information for displaying to user
"""
@login_required(login_url='/accounts/login/')
def sellStock(request, pk):
	owned_inst = get_object_or_404(OwnedStock, id=pk)
	currTrader = get_object_or_404(Trader, user=request.user)

	apiCaller = stockdata()
	symbol = owned_inst.stock.symbol
	quote = apiCaller.getQuotes([symbol])
	print(quote)
	price = quote[symbol]['price']
	revenue = float(price)*float(owned_inst.quantity)
	profit = revenue-float(owned_inst.price_at_purchase)*float(owned_inst.quantity)

	if request.method == 'POST':

		# Create a form instance and populate it with data from the request (binding):
		form = SellStockForm(request.POST)
		
		if form.is_valid():
			currTrader.cash += revenue
			currTrader.save()
			owned_inst.delete()
			return HttpResponseRedirect(reverse('portfolio') )
	else:
		form = SellStockForm()



	return render(request, 'confirm_sell.html', 
		{'form': form, 
		'ownedstock':owned_inst, 
		'price':price, 
		'revenue':revenue, 
		'profit':profit, 
		'trader':currTrader})

"""
Function for creating the deposit cash form and validating the amount
"""
@login_required(login_url='/accounts/login/')
def depositCash(request):
	currTrader = get_object_or_404(Trader, user=request.user)
	cash = currTrader.cash

	# If this is a POST request then process the Form data
	if request.method == 'POST':

		# Create a form instance and populate it with data from the request (binding):
		form = DepositCashForm(request.POST)

		# Check if the form is valid:
		if form.is_valid():

			currTrader.cash += form.cleaned_data['deposit']
			currTrader.save()

			# redirect to a new URL:
			return HttpResponseRedirect(reverse('portfolio') )

	# If this is a GET (or any other method) create the default form.
	else:
		form = DepositCashForm()

	return render(request, 'deposit.html', {'form': form, 'trader':currTrader})


"""
Function for creating the withdraw cash form and validating the amount
Note that this will allow the user to fall into a negative balance
"""
@login_required(login_url='/accounts/login/')
def withdrawCash(request):
	currTrader = get_object_or_404(Trader, user=request.user)
	cash = currTrader.cash

	# If this is a POST request then process the Form data
	if request.method == 'POST':

		# Create a form instance and populate it with data from the request (binding):
		form = WithdrawCashForm(request.POST)

		# Check if the form is valid:
		if form.is_valid():

			currTrader.cash -= form.cleaned_data['withdraw']
			currTrader.save()

			# redirect to a new URL:
			return HttpResponseRedirect(reverse('portfolio') )

	# If this is a GET (or any other method) create the default form.
	else:
		form = WithdrawCashForm()

	return render(request, 'deposit.html', {'form': form, 'trader':currTrader})

