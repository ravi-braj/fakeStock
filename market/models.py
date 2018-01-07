#Models that are used for the market trading app

from django.db import models
from django.urls import reverse
import uuid
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save


"""
Model that supplements the generic User model.
Used for storing information about cash balance
"""

class Trader(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="unique ID for trader")
	cash = models.FloatField()
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def value(self):
		stocks = OwnedStock.objects.filter(owner=self.user)
		currValue = 0
		for owned in stocks:
			currValue += float(owned.quantity)*float(owned.price_at_purchase)
		return currValue

# functions to make sure that a Trader gets created and updated whenever a user gets created/updated
# sets the default cash for each trader to be 5
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Trader.objects.create(user=instance, cash=5)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.trader.save()

"""
model for representing stocks. Used to store the offline list of symbols to call to the alpha Q API and their corresponding names
"""
class Stock(models.Model):
	name = models.CharField(max_length = 250, help_text="Enter the name of stock")
	symbol = models.CharField(max_length = 20, help_text = "Enter the stocks name")

	def get_absolute_url(self):
		return reverse('stock-detail', args=[str(self.symbol)])

	def __str__(self):
		return self.symbol


"""
Model for tracking the holdings of a user
"""
class OwnedStock(models.Model):
	stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
	time_of_purchase = models.DateTimeField(null=True)
	price_at_purchase = models.FloatField()
	owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	quantity = models.IntegerField(null=True)

	def __str__(self):
		return self.stock.symbol

	#constructor
	@classmethod
	def create(cls, stock, quantity, owner, price):
		owned = cls(quantity=quantity, owner=owner, price_at_purchase=price, stock=stock)
		return owned



