from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import os
import xml.etree.ElementTree as ET
from datetime import date, timedelta


def convert(request, amount, src_currency, dest_currency, reference_date):

	verify = verify_date(reference_date)
	if not verify["status"]:
		return JsonResponse({
			"status": "ko",
			"message": verify["message"]
		})
	
	file_path = os.path.join(settings.DATA_DIR, 'rates.xml')
	
	tree = ET.parse(file_path)

	root = tree.getroot()

	conversions = root[2]

	data = conversions[get_index(reference_date)]

	rates = parse_rates(data)

	if src_currency not in rates:
		return JsonResponse({
			"status": "ko",
			"message": "the src_currency field is invalid"
		})
	elif dest_currency not in rates:
		return JsonResponse({
			"status": "ko",
			"message": "the dest_currency field is invalid"
		})
	else:
		rate = rates[dest_currency] / rates[src_currency]
		result = float(amount) * rate
		return JsonResponse({
			"amount": result,
			"currency": dest_currency
		})
	

def verify_date(reference_date):
	reference_date = format_date(reference_date)
	message = "ok"

	is_past = date.today() >= reference_date
	if not is_past:
		message = "the reference_date field must be in the past"

	is_in_xml = reference_date >= date.today() - timedelta(days=90)
	if not is_in_xml:
		message = "the reference_date field must be maximum 90 days old"

	is_weekday = reference_date.weekday() < 4
	if not is_weekday:
		message = "the reference_date field must be a weekday (not weekends)"
	
	return {
		"status": is_past and is_in_xml and is_weekday,
		"message": message
	}


def get_index(reference_date):
	offset = date.today()
	weekday = offset.weekday()
	if weekday > 4:
		offset -= timedelta(days=weekday-4)
	return (offset - format_date(reference_date)).days


def format_date(reference_date):
    reference_date = reference_date.split('-')
    return date(int(reference_date[0]), int(reference_date[1]), int(reference_date[2]))


def parse_rates(rates):
	parsed = {"EUR": 1.0}
	for currency in rates:
		parsed[currency.attrib["currency"]] = float(currency.attrib["rate"])
	return parsed
