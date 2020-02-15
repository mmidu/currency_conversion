from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import xml.dom.minidom

def convert(request, amount, src_currency, dest_currency, reference_date):
	'''
	URL EXAMPLE
	http://localhost:8080/convert/amount=12.12/src_currency=DES/dest_currency=ASD/reference_date=1234-12-12

	'''
	file_path = os.path.join(settings.DATA_DIR, 'rates.xml')
	doc = xml.dom.minidom.parse(file_path);
	data = {
		"status": "ok", 
		"message": {
			"amount": amount,
			"src_currency": src_currency,
			"dest_currency": dest_currency,
			"reference_date": reference_date
		},
		"data": doc.nodeName
	}
	return JsonResponse(data)