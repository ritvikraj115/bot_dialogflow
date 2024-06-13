from flask import Flask,request,jsonify
import requests
import os


app= Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data= request.get_json()
    print(data)
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
    url="https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=cc34cec85455141c0e4a".format(source,target)
    response = requests.get(url)
    response= response.json()
    print(response)

    return response['{} {}'.format(source,target)]

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)
