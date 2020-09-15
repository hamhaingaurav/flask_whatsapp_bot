from flask import Flask, request, jsonify, make_response

from wabot import WaBot


app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    if request.method == 'POST':
        bot = WaBot(request.json)
        return bot.processing()


if(__name__) == '__main__':
    app.run()