from django.db import models

class Conversion(models.Model):
	amount = models.FloatField()
	src​_currency = models.CharField(max_length=3)
	dest_currency = models.CharField(max_length=3)
	reference_date = models.DateField(input_formats='%Y-%m-%d')