import requests

#TODO сделать конкретнве ошибки и чтоб в случае необходимости возвращал obj.json() {Для бесед и сообщений}
def check_errors(func):
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        if res.status_code != 200:
            raise requests.ConnectionError('Not 200 code')
        return res
    return inner


class Connect:
    def __init__(self, hostname, login, password):
        self.hostname = hostname
        self.login = login
        self.password = password

    @check_errors
    def get_token(self):
        token = requests.get(self.hostname + '/login?login={}&password={}'.format(
            self.login, self.password))
        self.token = token.text
        return token

    @check_errors
    def register(self):
        response = requests.get(self.hostname + '/register?login={}&password={}'.format(
            self.login, self.password))
        return response

    @check_errors
    def new_thread(self, username):
        response = requests.get(self.hostname + '/new_thread?token={}&username={}'.format(
            self.token, username))
        return response

    @check_errors
    def send_message(self, thread_id, text):
        response = requests.get(self.hostname + '/send_message?token={}&text={}&thread_id={}'.format(
            self.token, text, thread_id))
        return response

    @check_errors
    def get_threads(self):
        """Return requsts object. obj.json() need

        Returns:
            response
        """
        threads = requests.get(self.hostname + '/get_threads?token={}'.format(
            self.token))
        return threads

    @check_errors
    def get_messages(self, thread_id):
        """Return requsts object. obj.json() need

        Args:
            thread_id (int)

        Returns:
            response
        """
        messages = requests.get(self.hostname + '/get_messages?token={}&thread_id={}'.format(
            self.token, thread_id))
        return messages
