from flask import Flask, request
from flask_cors import CORS
from flask_mail import Mail, Message
import os


mail = Mail()

def create_app():
    new_app = Flask(__name__)
    cors_app = CORS(new_app)

    new_app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    new_app.config['MAIL_PORT'] = 465
    new_app.config['MAIL_USE_TLS'] = False
    new_app.config['MAIL_USE_SSL'] = True
    new_app.config['MAIL_USERNAME'] = "email"
    new_app.config['MAIL_PASSWORD'] = 'contraseña'
    new_app.config['MAIL_DEFAULT_SENDER'] = 'email'

    mail.init_app(new_app)

    @new_app.route("/")
    def home_page():
        request_query = request.args
        if request_query:

            response = ["Counter Server Working (Not that counter...)", "<ul>"]

            for arg, value in request_query.items():
                response.append(f"<li>{arg}: {value}</li>")

            response.append("</ul>")

            response = "".join(response)

            return response

        return "Product API Server Working (Not that counter...)"

    from product_api_service.database import cli_setup

    new_app.cli.add_command(cli_setup.db_setup)

    from product_api_service.api import service_api

    new_app.register_blueprint(service_api)

    return new_app
