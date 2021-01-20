from api_services import cheap_payment_service, expensive_payment_service, premium_payment_service
from utils.constant import PaymentGatewayType


def process_payment(payment_details):
    amount = payment_details.get("amount")
    payment_method = None
    payment_status = False
    transaction_id = None
    if amount <= 20:
        payment_status, transaction_id = cheap_payment_service.process_payment(payment_details)
        payment_method = PaymentGatewayType.CHEAP_PAYMENT_GATEWAY.value

    elif amount > 20 and amount <= 500:
        payment_status, transaction_id = expensive_payment_service.process_payment(payment_details)
        payment_method = PaymentGatewayType.EXPENSIVE_PAYMENT_GATEWAY.value
        if not payment_status:
            payment_status, transaction_id = cheap_payment_service.process_payment(payment_details)
            payment_method = PaymentGatewayType.CHEAP_PAYMENT_GATEWAY.value
    elif amount > 500:
        try_count = 0
        while try_count != 3:
            payment_status, transaction_id = premium_payment_service.process_payment(payment_details)
            if payment_status:
                break
            else:
                try_count += 1
        payment_method = PaymentGatewayType.PREMIUM_PAYMENT_GATEWAY.value
    payment_details["payment_status"] = payment_status
    payment_details["payment_method"] = payment_method
    payment_details["transaction_id"] = transaction_id
    return payment_details
