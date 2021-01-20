import random
import uuid


def process_payment(payment_details):
    random_number = random.randint(1, 10)
    if random_number > 7:
        return False, None
    else:
        return True, str(uuid.uuid4())
