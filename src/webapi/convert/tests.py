from django.test import TestCase
import requests
from .models import Conversion
from datetime import date, timedelta

class ConvertTest(TestCase):


	def setUp(self):
		self.conversion = Conversion(1, "EUR", "USD", date.today().strftime("%Y-%m-%d"))

	def test_verify_api(self):
		data = requests.get('http://localhost:8000/convert/amount=1/src_currency=EUR/dest_currency=EUR/reference_date=2020-02-14').json()
		self.assertEqual(data['amount'],1)
		self.assertEqual(data['currency'], 'EUR')


	def test_make_response(self):
		self.assertEqual({"status": "ok", "message": "msg"}, self.conversion.make_response("ok", "msg"))


	def test_format_date(self):
		today = date.today()
		dt = today.strftime("%Y-%m-%d")
		self.assertEqual(today, self.conversion.format_date(dt))


	def test_get_dates(self):
		dates = self.conversion.get_dates()
		
		today = date.today()
		if today.weekday() > 4:
			today = today - timedelta(days=today.weekday() - 4)
		dt = today.strftime("%Y-%m-%d")

		self.assertEqual(dt, dates[0].attrib['time'])


	def test_parse_rates(self):
		dates = self.conversion.get_dates()
		rates = self.conversion.parse_rates(dates[0])
		self.assertIn("EUR", rates)
		self.assertEqual(1.0, rates["EUR"])


	def test_verify_date_fails_on_future(self):
		conv = Conversion(1, "EUR", "USD", (date.today()+timedelta(days=1)).strftime("%Y-%m-%d"))
		response = conv.verify_date()
		self.assertEqual(False, response["status"])


	def test_verify_date_fails_on_oldest_than_ninety_days(self):
		conv = Conversion(1, "EUR", "USD", (date.today()-timedelta(days=91)).strftime("%Y-%m-%d"))
		response = conv.verify_date()
		self.assertEqual(False, response["status"])


	def test_verify_date_fails_on_weekends(self):
		conv = Conversion(1, "EUR", "USD", date(2020, 2, 16).strftime("%Y-%m-%d"))
		response = conv.verify_date()
		self.assertEqual(False, response["status"])
