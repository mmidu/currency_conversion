from django.db import models

class Conversion(models.Model):
	amount = models.FloatField()
	src_currency = models.CharField(max_length=3)
	dest_currency = models.CharField(max_length=3) 
	reference_date = DateTimeField()

	def __init__(self, amount, src_currency, dest_currency, reference_date):
		self.amount = amount
		self.src_currency = src_currency
		self.dest_currency = dest_currency
		self.reference_date = reference_date

	def convert(self):
		result = self.amount * self.dest_rate / self.src_rate

		"amount": result,
		"currency": dest_currency,