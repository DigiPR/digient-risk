from flask import Flask
import threading
from risk_client import RiskClient

app = Flask(__name__)
threading.Thread(target=RiskClient).start()


@app.route('/')
def welcome():
    return "Welcome to Camunda Python Client"


if __name__ == '__main__':
    app.run()
