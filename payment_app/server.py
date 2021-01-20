from flask import Flask
from controller.apis_controller import payment_blueprint

app = Flask(__name__)

app.register_blueprint(payment_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
