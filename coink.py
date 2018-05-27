from flask import Flask, request, render_template
import json
import requests
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

  
  
# app = Flask(__name__)
# # bootstrap = Bootstrap(app)

URL = "https://openexchangerates.org//api/latest.json?app_id=3792aac73c0d4da982217fcfbaf18cce"

DEFAULTS = { 'currency_have':'GBP', 'currency_want':'USD', 'quantity': 100}

@app.route("/")
def home():
    quantity = request.args.get("quantity")
    if not quantity:
        currency_have = DEFAULTS['quantity']
    currency_have = request.args.get("currency_have")
    if not currency_have:
        currency_have = DEFAULTS['currency_have']
    currency_want = request.args.get("currency_want")
    if not currency_want:
        currency_want = DEFAULTS['currency_want']
    conversion, currencies = get_rate(currency_have, currency_want)
    return render_template("index.html", currency_have=currency_have, currency_want=currency_want, conversion=conversion, currencies=sorted(currencies))

def get_rate(have, want):
    r = requests.get(URL)
    r = r.json()
    rates = r['rates']
    have = rates[have.upper()]
    want = rates[want.upper()]
    quantity = request.args.get("quantity")
    return (int(quantity) * (want / have), rates.keys())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)