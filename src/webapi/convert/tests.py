from django.test import TestCase
import requests

class ConvertTest(TestCase):

	def test_verify_api(self):
		data = requests.get('http://localhost:8000/convert/amount=1/src_currency=EUR/dest_currency=EUR/reference_date=2020-02-14').json()
		self.assertEqual(data['amount'],1)
		self.assertEqual(data['currency'], 'EUR')
