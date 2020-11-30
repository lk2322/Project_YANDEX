import flask
import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
import jwt
import datetime
import os
import time
import dotenv


# Const check
dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    print('SECRET_KEY ERROR')
    exit()
HOST = os.getenv("HOST_IP")
if not HOST:
    print('HOST_IP ERROR')
    exit()


# Error const
INVALID_TOKEN_ERROR = 'invalid token'


app = flask.Flask(__name__)


def exp_tommorow():
    return datetime.datetime.now() + datetime.timedelta(days=1)


def check_token(token: str):
    """Проверка jwt токена

    Args:
        token (str):

    """
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        # Проверка на время действия токена
        if user['exp'] < time.time():
            return
        else:
            return user
    except jwt.exceptions.DecodeError:
        return


def check_valid(func):
    """Декоратор для проверки валидности токена
    """
    def check_token_decorator(*args, **kwargs):
        args_f = flask.request.args
        token = args_f['token']
        user = check_token(token)
        flask.request.user = user
        if not user:
            return flask.abort(400, INVALID_TOKEN_ERROR)
        return func(*args, **kwargs)
    return check_token_decorator


@app.route('/login')
def check_login():
    args = flask.request.args
    login = args['login']
    passw = args['password']
    user = db.get_user(login)
    try:
        if check_password_hash(user.pwhash, passw):
            return jwt.encode({'username': login, 'user_id': user.id, 'exp': exp_tommorow()},
                              SECRET_KEY, algorithm='HS256')
    except AttributeError:
        return flask.abort(400, 'Check password or username')


@app.route('/register')
def register():
    args = flask.request.args
    login = args['login']
    passw = args['password']
    if db.get_user(login):
        return flask.abort(400, 'username_exists')
    db.create_user(login, generate_password_hash(passw))
    return 'ok'


@app.route('/new_thread', endpoint='create_thread')
@check_valid
def create_thread():
    args = flask.request.args
    username = args['username']
    user = flask.request.user
    try:
        db.create_thread(user['username'], username)
    except Exception:
        return flask.abort(400, 'user not found')
    return 'ok'


@app.route('/send_message', endpoint='send_message')
@check_valid
def send_message():
    args = flask.request.args
    text = args['text']
    thread_id = args['thread_id']
    user = flask.request.user
    db.create_message(text, thread_id, user['user_id'])
    return 'ok'


@app.route('/get_threads', endpoint='get_thread')
@check_valid
def get_thread():
    user = flask.request.user
    return db.get_threads(user['user_id'])


@app.route('/get_messages', endpoint='messages')
@check_valid
def messages():
    thread_id = flask.request.args['thread_id']
    return db.get_messages(thread_id)


if __name__ == "__main__":
    app.run(HOST, 80)
