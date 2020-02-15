from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import xml.etree.ElementTree as ET

def convert(request, amount, src_currency, dest_currency, reference_date):
	file_path = os.path.join(settings.DATA_DIR, 'rates.xml')
	
	tree = ET.parse(file_path)

	root = tree.getroot()

	src_rate = 0
	dest_rate = 0
	rate = 0
	result = 0

	for date in root[2]:
		if date.attrib['time'] == reference_date:
			for currency in date:
				if currency.attrib['currency'] == src_currency:
					src_rate = float(currency.attrib['rate'])
				elif currency.attrib['currency'] == dest_currency:
					dest_rate = float(currency.attrib['rate'])
	
	if src_currency == 'EUR':
		src_rate = 1
	elif dest_currency == 'EUR':
		dest_rate = 1 

	if dest_rate != 0 and src_rate != 0:
		rate = dest_rate / src_rate
		result = float(amount) * rate

	data = {
		"amount": result,
		"currency": dest_currency,
	}

	return JsonResponse(data)