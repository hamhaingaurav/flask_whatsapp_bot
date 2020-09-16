from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re

from wabot import WaBot



#App configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'fake_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



# Model for saving the chats into the database
class Questions(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return str(self.question)

class Products(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    rate = db.Column(db.Numeric, nullable=False)
    unit = db.Column(db.String(10), nullable=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now)
    purchases = db.relationship('Purchases', backref='product')

    def __repr__(self):
        return str(self.name)

class Users(db.Model):
    id_ = db.Column('id', db.String(20), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    restaurant_name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    contact = db.Column(db.Integer, nullable=True)
    last_login = db.Column(db.DateTime, nullable=False, default=datetime.now)
    purchases = db.relationship('Purchases', backref='user')

    def __repr__(self):
        return str(self.chat_id)

class Purchases(db.Model):
    id_ = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"{self.product_id} by {self.user_id}"



#Routes and their logic function
@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':

        questions = Questions.query.all()
            
        q_data = {
            'welcome_string': """Welcome to the Gaurav's Shop\n\nAre you here to buy fresh items directly from the farm ?\n\nEnter 'Yes'.""",
            'congrats_message': """Congratulations, Your order has been placed.\n\nDo check out our Gaurav's Shop app at Playstore for more fresh items directly from farms.\n\nHere is the link:\nhttp://goo.gl/gaurav"""
        }

        products_list = Products.query.all()
        price_list = f"Price list\n\n" + " \n".join([f"{product.id_}. {product.name} INR - {product.rate}/{product.unit}" for product in products_list])

        bot = WaBot()

        dict_messages = request.json['messages']

        if dict_messages != []:
            for message in dict_messages:
                text = message['body']
                text_list = text.split()

                if not message['fromMe']:
                    id  = message['chatId']

                    if text_list[0].lower() in ['hi', 'hello', 'hey', 'namaste',]:
                        return bot.welcome(id, q_data=q_data)
                    elif text_list[0].lower() == 'chatid':
                        return bot.show_chat_id(id)
                    elif text_list[0].lower()=='yes':
                        que = questions[0].question
                        return bot.ask_question(id, que=que)
                    elif re.search("^(Name)\ [A-Za-z ]+$", text):
                        # user_obj.username = text.split("Name ")[1]
                        que = questions[1].question
                        #Save username
                        return bot.ask_question(id, que=que)
                    elif re.search("^(Restaurant)\ [A-Za-z0-9 ]+$", text):
                        # Save Restaurant Name
                        que = questions[2].question
                        return bot.ask_question(id, que=que)
                    elif re.search("^(Address)\ [A-Za-z0-9,\- ]+$", text):
                        # Save Address
                        que = questions[3].question
                        return bot.ask_question(id, que=que)
                    elif re.search("^(Age)\ [0-9]+$", text):
                        # Save Age
                        que = questions[4].question
                        return bot.ask_question(id, que=que)
                    elif re.search("^(Contact)\ [0-9]{10}$", text):
                        # Save Contact
                        que = questions[5].question
                        return bot.ask_question(id, que=que)
                    elif re.search("^(ToldBy)\ [A-Za-z]+$", text):
                        que = q_data['congrats_message']
                        return bot.ask_question(id, que=que)
                    elif re.search("(\d+\ \d+[A-Za-z\ ]{1,}){1,}", text):
                        return bot.send_order_confirmation(id, q_data=q_data)
                else:
                    return 'NoCommand'

    elif request.method == 'GET':

        response = make_response('<h1>Welcome to the Whatsapp Bot Build by Gaurav</h1>', 200)
        response.mimetype = "text/html"
        return response


if(__name__) == '__main__':
    app.run()