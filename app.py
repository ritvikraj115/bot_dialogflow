from flask import Flask,request,jsonify
import requests
import os
import logging
import currencyapicom


app= Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    logging.basicConfig(level=logging.INFO)
    data= request.get_json()
    # app.logger.info(data)
    source_currency= data['queryResult']['parameters']['unit-currency']['currency']
    amount=data['queryResult']['parameters']['unit-currency']['amount']
    target_currency=data['queryResult']['parameters']['currency-name']


    cf= fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount*cf
    final_amount= round(final_amount,1)

    response={
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source,target):
    client = currencyapicom.Client('cur_live_FJSZpNZ5ykTrusCMNOPlnpeByAGBiVamn0nArCZB')
    result = client.latest(source,currencies=[target])
    app.logger.info(result['data'][target]['value'])

    return result['data'][target]['value']

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable or default to 5000
    app.logger.info(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port)
