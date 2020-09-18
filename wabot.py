import json
import requests
from env import API_URL, TOKEN

class WaBot:
    def __init__(self):
        self.APIUrl = API_URL
        self.token = TOKEN

    def send_requests(self, method, data):
        url = f"{self.APIUrl}{method}?token={self.token}"
        headers = {'Content-type': 'application/json'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatId, text):
        data = {"chatId" : chatId, "body" : text}
        answer = self.send_requests('sendMessage', data)
        return answer

    def show_chat_id(self, chatId):
        return self.send_message(chatId, f"Chat ID : {chatId}")

    def welcome(self, chatId, que):
        return self.send_message(chatId, que)

    def ask_question(self, chatId, que):
        return self.send_message(chatId, que)

    def send_order_confirmation(self, chatId, que):
        return self.send_message(chatId, que)

    # def no_response(self, chatId):
    #     return self.send_message(chatId, "Sorry, We could not understand you, Please try again !")