from datetime import datetime


def validate_credit_card(credit_card_number):
    digits = [int(c) for c in credit_card_number if c.isdigit()]
    checksum = digits.pop()
    digits.reverse()
    doubled = [2 * d for d in digits[0::2]]
    total = sum(d - 9 if d > 9 else d for d in doubled) + sum(digits[1::2])
    return (total * 9) % 10 == checksum


def validate_date_time(date_time):
    try:
        d0 = datetime.strptime(date_time, '%d/%m/%Y')
        d1 = datetime.now()
        delta = d0 - d1
        if delta.days < 0:
            return False
        else:
            return True
    except Exception as e:
        print("ERROR:", "validate_date_time", e)
        return False


def validate_amount(amount):
    try:
        amount = float(amount)
        if amount > 0:
            return True
        else:
            return False
    except Exception as e:
        print("ERROR:", "validate_amount", e)
        return False


def validate_security_code(security_code):
    if len(str(security_code)) == 3 and security_code.isdigit():
        return True
    else:
        return False
