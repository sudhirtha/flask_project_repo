from flask_app_mvc_webservices.hotelcontroller import *
from flask_app_mvc_webservices.roomcontroller import *
from flask_app_mvc_webservices.accountcontroller import *
from flask_app_mvc_webservices.menucontroller import *
from flask_app_mvc_webservices.customers_controller import *
from flask_app_mvc_webservices.logincontroller import *

if __name__ == '__main__':
    app.run(debug=True)