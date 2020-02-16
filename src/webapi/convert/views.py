from django.shortcuts import render
from django.http import JsonResponse
from .models import Conversion

def convert(request, amount, src_currency, dest_currency, reference_date):
	conversion = Conversion(amount, src_currency, dest_currency, reference_date)
	return JsonResponse(conversion.convert())