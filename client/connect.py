import requests


class Connect:
    def __init__(self, hostname, login, password):
        self.hostname = hostname
        self.login = login
        self.password = password

    def get_token(self):
        token = requests.get(self.hostname + '/login?login={}&password={}'.format(
            self.login, self.password))
        self.token = token.text

    def register(self):
        response = requests.get(self.hostname + '/register?login={}&password={}'.format(
            self.login, self.password))
        if response.text == 'ok':
            self.get_token()

    def new_thread(self, username):
        requests.get(self.hostname + '/new_thread?token={}&username={}'.format(
            self.token, username))

    def send_message(self, thread_id, text):
        requests.get(self.hostname + '/send_message?token={}&text={}&thread_id={}'.format(
            self.token, text, thread_id))

    def get_threads(self):
        threads = requests.get(self.hostname + '/get_threads?token={}'.format(
            self.token))
        return threads.json()

    def get_messages(self, thread_id):
        messages = requests.get(self.hostname + '/get_messages?token={}thread_id={}&'.format(
            self.token, thread_id))
        return messages.json()
