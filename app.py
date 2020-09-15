from flask import Flask, request, make_response

from wabot import WaBot


app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        bot = WaBot(request.json)
        return bot.processing()
    elif request.method == 'GET':
        response = make_response('<h1>Welcome to the Whatsapp Bot Build by Gaurav</h1>', 200)
        response.mimetype = "text/html"
        return response


if(__name__) == '__main__':
    app.run()