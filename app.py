from flask import Flask

from routes.auth import auth
from routes.home import home
from routes.customer import customer
from routes.account import account
from routes.transaction import transaction

from static.python.paths import files as file, routes as route
# print("file: ", file['login'])
# print("route: ", route)

# App
app = Flask(__name__)
app.config['SECRET_KEY'] = "mysecretkey"

# Blueprints
app.register_blueprint(auth)
app.register_blueprint(home)
app.register_blueprint(customer)
app.register_blueprint(account)
app.register_blueprint(transaction)

############################# Context Processor #############################
@app.context_processor
def load_data():
    return {'route': route}

############################ App ############################
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    # app.run(host="0.0.0.0", port=5000)
