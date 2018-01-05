#all the forms required for market app

from django import forms
from django.forms import ModelForm
from .models import Stock, OwnedStock, User, Trader
from django.core.exceptions import ValidationError
import datetime


class BuyStockForm(forms.Form):
	quantity = forms.IntegerField()


	def clean_quantity(self):
		data = self.cleaned_data['quantity']
		return data

"""
No fields required for selling stock
This is included as a form to provide future scope for adding things to this form and for consistency
"""
class SellStockForm(forms.Form):
	pass


"""
Form for depositing cash. Only requires a float between 0 and 1000000
"""
class DepositCashForm(forms.Form):
	deposit = forms.FloatField()

	def clean_deposit(self):
		data = self.cleaned_data['deposit']

		if data<=0 or data>1000000:
			raise ValidationError('Please select an amount between 0 and 1 000 000')

		return data

"""
Form for withdrawing cash. Only requres a float between 0 and 1000000
"""
class WithdrawCashForm(forms.Form):
	withdraw = forms.FloatField()

	def clean_withdraw(self):
		data = self.cleaned_data['withdraw']
		if data<=0 or data>1000000:
			raise ValidationError('Please select an amount between 0 and 1 000 000')

		return data