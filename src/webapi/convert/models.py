from django.db import models
from django.conf import settings
import os
import xml.etree.ElementTree as ET
from datetime import date, timedelta


class Conversion():
	managed = False

	def __init__(self, amount, src_currency, dest_currency, reference_date):
		self.amount = float(amount)
		self.src_currency = src_currency
		self.dest_currency = dest_currency
		self.reference_date = self.format_date(reference_date)


	def convert(self):
		message = ''
		check_date = self.verify_date()

		if check_date["status"]:
			dates = self.get_dates()

			self.rates = self.parse_rates(dates[self.get_date_index()])

			check_currencies = self.verify_currencies()

			if check_currencies["status"]:
				return self.make_result()
			else:
				message = check_currencies["message"]
		else:
			message = check_date["message"]

		return self.make_response("ko", message)


	def verify_date(self):
		message = "ok"

		is_past = date.today() >= self.reference_date
		is_in_xml = self.reference_date >= date.today() - timedelta(days=90)
		is_weekday = self.reference_date.weekday() < 5

		if not is_past:
			message = "the reference_date field must be in the past"

		if not is_in_xml:
			message = "the reference_date field must be maximum 90 days old"

		if not is_weekday:
			message = "the reference_date field must be a weekday (not weekends)"

		return {
			"status": is_past and is_in_xml and is_weekday,
			"message": message
		}


	def get_dates(self):

		file_path = os.path.join(settings.DATA_DIR, 'rates.xml')
		tree = ET.parse(file_path)
		root = tree.getroot()

		return root[2]


	def parse_rates(self, rates):

		parsed = {"EUR": 1.0}

		for currency in rates:
			parsed[currency.attrib["currency"]] = float(currency.attrib["rate"])

		return parsed


	def get_date_index(self):

		offset = date.today()
		weekday = offset.weekday()

		if weekday > 4:
			offset -= timedelta(days=weekday-4)

		return (offset - self.reference_date).days


	def verify_currencies(self):
		message = ""

		src_in_rates = self.src_currency in self.rates
		dest_in_rates = self.dest_currency in self.rates

		if not src_in_rates:
			message =  "the src_currency field is invalid"
		
		if not dest_in_rates and not src_in_rates:
			message += ", the dest_currency field is invalid"
		elif not dest_in_rates:
			message = "the dest_currency field is invalid"

		return {
			"status": src_in_rates and dest_in_rates,
			"message": message
		}


	def format_date(self, reference_date):

	    reference_date = reference_date.split('-')

	    return date(int(reference_date[0]), int(reference_date[1]), int(reference_date[2]))


	def make_response(self, status, message):
		return {
			"status": status,
			"message": message
		}


	def make_result(self):
		rate = self.rates[self.dest_currency] / self.rates[self.src_currency]
		result = float(self.amount) * rate

		return {
			"amount": round(result, 2),
			"currency": self.dest_currency,
		}
