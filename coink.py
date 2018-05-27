from flask import Flask, request, render_template
import json
import requests

app = Flask(__name__)

URL = "https://openexchangerates.org//api/latest.json?app_id=3792aac73c0d4da982217fcfbaf18cce"

DEFAULTS = { 'currency_have':'GBP','currency_want':'USD' }

@app.route("/")
def home():
    currency_have = request.args.get("currency_have")
    if not currency_have:
        currency_have = DEFAULTS['currency_have']
    currency_want = request.args.get("currency_want")
    if not currency_want:
        currency_want = DEFAULTS['currency_want']
    rate, currencies = get_rate(currency_have, currency_want)
    return render_template("index.html", currency_have=currency_have, currency_want=currency_want, rate=rate, currencies=sorted(currencies))

def get_rate(have, want):
    r = requests.get(URL)
    r = r.json()
    rates = r['rates']
    have = rates[have.upper()]
    want = rates[want.upper()]
    return (want / have, rates.keys())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)