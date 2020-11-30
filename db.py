from peewee import *
from typing import List
import datetime

db = SqliteDatabase('main.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True)
    pwhash = CharField()


class Thread(BaseModel):
    pass


class Participant(BaseModel):
    thread_id = ForeignKeyField(Thread, backref='participant')
    user_id = ForeignKeyField(User)


class Message(BaseModel):
    thread_id = ForeignKeyField(Thread, backref='messages')
    user_id = ForeignKeyField(User)
    text = CharField()
    time = DateTimeField()


def get_user(login: str):
    db.connect(reuse_if_open=True)
    try:
        user = User.get(User.username == login)
    except Exception:
        return
    db.close()
    return user


def create_thread(*usrnames: List[int]):
    db.connect(reuse_if_open=True)
    thread = Thread.create()
    for i in usrnames:
        Participant.create(thread_id=thread, user_id=User.get(User.username == i))
    db.close()


def get_threads(user_id: int):
    threads = Thread.select().join(Participant).where(Participant.user_id == user_id)
    threads_dict = {}
    for i in threads:
        for j in i.participant:
            if j.user_id.id == user_id:
                continue
            # {имя: id беседы}
            threads_dict[j.user_id.username] = i.id
    return threads_dict


def get_messages(thread_id: int) -> dict:
    messages = Message.select().where(Message.thread_id == thread_id).order_by(Message.time)
    messages_dict = {}
    for i in messages:
        messages_dict[i.id] = {'datetime': i.time,
                               'text': i.text,
                               'user_id': i.user_id.id,
                               'username': i.user_id.username}
    return messages_dict


def create_message(text: str, thread_id: int, from_id: int) -> None:
    db.connect(reuse_if_open=True)
    Message.create(thread_id=thread_id, text=text,
                   user_id=from_id, time=datetime.datetime.now())
    db.close()


def create_user(login: str, pwhash: str):
    db.connect(reuse_if_open=True)
    User.create(username=login, pwhash=pwhash)
    db.close()


if __name__ == "__main__":
    db.create_tables([User, Thread, Participant, Message])
    a = get_threads(1)
    print(a)
