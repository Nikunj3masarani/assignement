from flask import Blueprint
from flask import request

from utils.response_helper import *
from validator import payment_request_validator
from controller import payment_controller
from utils import messages
import traceback
payment_blueprint = Blueprint('payment_blueprint', __name__)


@payment_blueprint.route('/process_payment', methods=["POST"])
def processPayment():
    try:
        if request.method == 'POST':
            status, data = payment_request_validator.validate_payment_request(request)
            if not status:
                return data
            else:
                payment_data = payment_controller.process_payment(data)
                return success(messages.PAYMENT_PROCESSED, payment_data)
        else:
            return method_not_allowed()
    except Exception as e:
        traceback.print_exc()
        print("ERROR:", "error_process_payment", str(e))
        return server_error()
