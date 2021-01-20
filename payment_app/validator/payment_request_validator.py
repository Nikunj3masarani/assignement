from utils import util, response_helper
from utils import messages


def validate_payment_request(request):
    data = request.json
    if not data:
        return False, response_helper.parameter_missing("credit_card_number")

    credit_card_number = data.get('credit_card_number')
    card_holder = data.get('card_holder')
    expiry_date = data.get('expiry_date')
    security_code = data.get('security_code')
    amount = data.get('amount')
    if credit_card_number == None or credit_card_number == "":
        return False, response_helper.parameter_missing("credit_card_number")
    elif card_holder == None or card_holder == "":
        return False, response_helper.parameter_missing("card_holder")
    elif expiry_date == None or expiry_date == "":
        return False, response_helper.parameter_missing("expiry_date")
    elif amount == None:
        return False, response_helper.parameter_missing("amount")
    elif not util.validate_credit_card(str(credit_card_number)):
        return False, response_helper.parameter_invalid(messages.INVALID_CREDIT_CARD)
    elif not util.validate_date_time(expiry_date):
        return False, response_helper.parameter_invalid(messages.INVALID_EXPIRY_DATE)
    elif not util.validate_amount(amount):
        return False, response_helper.parameter_invalid(messages.INVALID_AMOUNT)
    elif security_code and not util.validate_security_code(security_code):
        return False, response_helper.parameter_invalid(messages.INVALID_SECURITY_CODE)
    return True, {
        "credit_card_number": credit_card_number,
        "card_holder": card_holder,
        "expiry_date": expiry_date,
        "security_code": int(security_code) if security_code else None,
        "amount": float(amount)
    }
