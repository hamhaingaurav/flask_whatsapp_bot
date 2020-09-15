import json
import requests
import re
from env import API_URL, TOKEN

class WaBot:
    def __init__(self, json):
        self.json = json
        self.dict_messages = json['messages']
        self.APIUrl = API_URL
        self.token = TOKEN
        self.user_data = {
            'welcome_string': """Welcome to the Gaurav's Shop\n\nAre you here to buy fresh items directly from the farm ?\n\nEnter 'Yes'.""",
            'q1': ["""What is your name?\nNote: Please use only capital letters for your name!""", None],
            'q2': ["""What is the name of your restaurant?\nPlease  Enter in this format!\n\nRestaurant-Pizza Hut""", None],
            'q3': ["""What is your address?\n\nAddresss Format\nAddress Line 1\nAddress Line 2\nDistrict, State\nPin Code""", None],
            'price_list': """Price list\n\n1. Tomato    INR 20/KG\n2. Dhania    INR 50/KG\n3. Kiwi  INR 20/KG\n\nTo Place a Order, Enter in this format\nOption Number<space>Quantity in Kg\n E.g. - 2 10Kg""",
            'congrats_message': """Congratulations, Your order has been placed.\n\nDo check out our Gaurav's Shop app at Playstore for more fresh items directly from farms.\n\nHere is the link:\nhttp://goo.gl/gaurav"""
        }

    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatId, text):
        data = {"chatId" : chatId, "body" : text}
        answer = self.send_requests('sendMessage', data)
        return answer

    def welcome(self, chatId):
        welcome_string = self.user_data['welcome_string']
        return self.send_message(chatId, welcome_string)

    def ask_name(self, chatId):
        if  self.user_data['q1'][1] is None:
            return self.send_message(chatId, self.user_data['q1'][0])
        else:
            self.ask_restaurant_name(chatId)

    def ask_restaurant_name(self, chatId, name):
        self.user_data['q1'][1] = name
        if  self.user_data['q2'][1] is None:
            return self.send_message(chatId, self.user_data['q2'][0])
        else:
            self.ask_address(chatId)

    def ask_address(self, chatId, restaurant_name):
        self.user_data['q2'][1] = restaurant_name
        if  self.user_data['q3'][1] is None:
            return self.send_message(chatId, self.user_data['q3'][0])
        else:
            self.ask_address(chatId)

    def price_list(self, chatId, address):
        self.user_data['q3'][1] = address
        return self.send_message(chatId, self.user_data['price_list'])

    def send_order_confirmation(self, chatId):
        return self.send_message(chatId, self.user_data['congrats_message'])

    def show_chat_id(self, chatId):
        return self.send_message(chatId, f"Chat ID : {chatId}")


    def processing(self):
        if self.dict_messages != []:
            for message in self.dict_messages:
                body = message['body']
                text = body.split()
                if not message['fromMe']:
                    id  = message['chatId']
                    if text[0].lower() in ['hi', 'hello', 'hey', 'namaste',]:
                        return self.welcome(id)
                    elif text[0].lower() == 'chatid':
                        return self.show_chat_id(id)
                    elif text[0].lower()=='yes':
                        return self.ask_name(id)
                    elif body.upper() == body:
                        return self.ask_restaurant_name(id, name=body)
                    elif 'restaurant' in body.lower().split('-'):
                        return self.ask_address(id, restaurant_name=body)
                    elif re.search(".+\n.+\n.+\n.+", body.lower()):
                        return self.price_list(id, address=body)
                    elif re.search("(\d \d+(Kg|kg|KG|kG).*\n*){1,}", body):
                        return self.send_order_confirmation(id)
                else:
                    return 'NoCommand'