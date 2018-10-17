# coding=utf-8

import datetime
from decimal import Decimal


CUSTOMER_ID = "fake_customer_id"
CUSTOMER_EMAIL = "fake@email.com"
CLIENT_TOKEN = "fake_client_token"
SUBSCRIPTION_ID = "fake_subscription_id"
PLAN_ID = "fake_plan_id"
SUBSCRIPTION_STATUS = "Active"
SUBSCRIPTION_BALANCE = Decimal("123.45")
PAYMENT_METHOD_NONCE = "fake-valid-amex-nonce"
PAYMENT_METHOD_TOKEN = "fake_payment_method_token"


class Result(object):
    pass


class PaymentMethod(object):
    token = PAYMENT_METHOD_TOKEN


customer = {
    "id": CUSTOMER_ID,
    "company": None,
    "email": CUSTOMER_EMAIL,
    "fax": None,
    "first_name": None,
    "last_name": None,
    "merchant_id": None,
    "phone": None,
    "created_at": datetime.datetime.utcnow(),
    "updated_at": datetime.datetime.utcnow(),
    "website": None,
}

result_success = Result()
result_success.is_success = True

result_failure = Result()
result_failure.is_success = False
result_failure.message = "Fake error message"

result_customer_success = Result()
result_customer_success.is_success = True
result_customer_success.customer = customer

subscription = {
    "id": SUBSCRIPTION_ID,
    "plan_id": PLAN_ID,
    "status": SUBSCRIPTION_STATUS,
    "price": Decimal('10.00'),
    "balance": SUBSCRIPTION_BALANCE,
    "billing_day_of_month": 17,
    "current_billing_cycle": 1,
    "days_past_due": None,
    "payment_method_token": '5cftfn',
    "trial_duration": None,
    "trial_duration_unit": None,
    "trial_period": False,
    "created_at": datetime.datetime.utcnow(),
    "updated_at": datetime.datetime.utcnow(),
}


result_payment_method_success = Result()
result_payment_method_success.is_success = True
result_payment_method_success.payment_method = PaymentMethod()

result_subscription_success = Result()
result_subscription_success.is_success = True
result_subscription_success.subscription = subscription

result_payment_method_failure = Result()
result_payment_method_failure.is_success = False
result_payment_method_failure.message = "Fake error message"

result_subscription_failure = Result()
result_subscription_failure.is_success = False
result_subscription_failure.message = "Fake error message"
