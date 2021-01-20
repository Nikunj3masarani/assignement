import unittest
from server import app
import json
from utils import messages, constant


class BasicTestCase(unittest.TestCase):

    def test_api_exists(self):
        tester = app.test_client(self)
        response = tester.get('/payment', content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_api_allowed_method(self):
        tester = app.test_client(self)
        response = tester.get('/process_payment', content_type='application/json')
        self.assertEqual(response.status_code, 405)

    def test_valid_post_api(self):
        valid_request_body = {
            "credit_card_number": '4716727753614812',
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2023",
            "amount": "502",
            "security_code": "220"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=valid_request_body)
        self.assertEqual(response.status_code, 200)

    def test_empty_request_body(self):
        request_body = {}
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertNotEqual(response.status_code, 200)

    def test_missing_credit_card(self):
        request_body = {
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)

        self.assertEqual(response.json.get("message"), messages.PARAMETER_MISSING.format("credit_card_number"))
        self.assertEqual(response.status_code, 400)

    def test_missing_card_holder(self):
        request_body = {
            "credit_card_number": 4716727753614812
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("message"), messages.PARAMETER_MISSING.format("card_holder"))
        self.assertEqual(response.status_code, 400)

    def test_missing_expiry_date(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("message"), messages.PARAMETER_MISSING.format("expiry_date"))
        self.assertEqual(response.status_code, 400)

    def test_missing_amount(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2023"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("message"), messages.PARAMETER_MISSING.format("amount"))
        self.assertEqual(response.status_code, 400)

    def test_with_all_required_data(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2023",
            "amount": "100"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("message"), messages.PAYMENT_PROCESSED)
        self.assertEqual(response.status_code, 200)

    def test_invalid_credit_card(self):
        request_body = {
            "credit_card_number": 4716727753614811,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2023",
            "amount": "100"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("message"), messages.INVALID_CREDIT_CARD)
        self.assertEqual(response.status_code, 400)

    def test_invalid_expiry_date_format(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20-02-2023",
            "amount": "100"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("message"), messages.INVALID_EXPIRY_DATE)
        self.assertEqual(response.status_code, 400)

    def test_invalid_expiry_past_date(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2020",
            "amount": "100"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("message"), messages.INVALID_EXPIRY_DATE)
        self.assertEqual(response.status_code, 400)

    def test_invalid_expiry_amount(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2023",
            "amount": "10k"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("message"), messages.INVALID_AMOUNT)
        self.assertEqual(response.status_code, 400)

    def test_invalid_security_code_length(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2023",
            "amount": "100",
            "security_code": "11"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("message"), messages.INVALID_SECURITY_CODE)
        self.assertEqual(response.status_code, 400)

    def test_invalid_security_code(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2023",
            "amount": "100",
            "security_code": "11a"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("message"), messages.INVALID_SECURITY_CODE)
        self.assertEqual(response.status_code, 400)

    def test_valid_response_data_format(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2023",
            "amount": "100",
            "security_code": "110"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertNotEqual(response.json.get("message"), None)
        self.assertNotEqual(response.json.get("payload"), None)
        self.assertNotEqual(response.json.get("payload").get("credit_card_number"), None)
        self.assertEqual(response.json.get("payload").get("credit_card_number"), request_body.get("credit_card_number"))
        self.assertEqual(response.json.get("payload").get("amount"), float(request_body.get("amount")))
        self.assertNotEqual(response.json.get("payload").get("card_holder"), None)
        self.assertEqual(response.json.get("payload").get("card_holder"), request_body.get("card_holder"))
        self.assertNotEqual(response.json.get("payload").get("expiry_date"), None)
        self.assertEqual(response.json.get("payload").get("expiry_date"), request_body.get("expiry_date"))
        self.assertNotEqual(response.json.get("payload").get("security_code"), None)
        self.assertEqual(response.json.get("payload").get("security_code"), int(request_body.get("security_code")))
        self.assertEqual(response.json.get("payload").get("security_code"), int(request_body.get("security_code")))
        self.assertNotEqual(response.json.get("payload").get("payment_method"), None)
        self.assertNotEqual(response.json.get("payload").get("payment_status"), None)
        self.assertNotEqual(response.json.get("payload").get("transaction_id"), None)
        self.assertEqual(response.status_code, 200)

    def test_cheap_payment_gateway(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2023",
            "amount": 10,
            "security_code": "110"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("payload").get("payment_method"),
                         constant.PaymentGatewayType.CHEAP_PAYMENT_GATEWAY.value)
        self.assertEqual(response.status_code, 200)

    def test_expensive_payment_gateway(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2023",
            "amount": 401,
            "security_code": "110"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertIn(response.json.get("payload").get("payment_method"),
                      [constant.PaymentGatewayType.CHEAP_PAYMENT_GATEWAY.value,
                       constant.PaymentGatewayType.EXPENSIVE_PAYMENT_GATEWAY.value])
        self.assertEqual(response.status_code, 200)

    def test_premium_payment_gateway(self):
        request_body = {
            "credit_card_number": 4716727753614812,
            "card_holder": "Nikunj Masrani",
            "expiry_date": "20/02/2023",
            "amount": 1000,
            "security_code": "110"
        }
        tester = app.test_client(self)
        response = tester.post('/process_payment', content_type='application/json', json=request_body)
        self.assertEqual(response.json.get("payload").get("payment_method"),
                         constant.PaymentGatewayType.PREMIUM_PAYMENT_GATEWAY.value)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
