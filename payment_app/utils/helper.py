def credit_card_validator(card_number):
    digits = [int(c) for c in card_number if c.isdigit()]
    checksum = digits.pop()
    digits.reverse()
    doubled = [2 * d for d in digits[0::2]]
    total = sum(d - 9 if d > 9 else d for d in doubled) + sum(digits[1::2])
    return (total * 9) % 10 == checksum
