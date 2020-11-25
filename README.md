
<h3 align="center">Simple Messenger</h3>

<div>

[![Status](https://img.shields.io/badge/status-active-success.svg)]() [![GitHub Issues](https://img.shields.io/github/issues/lk2322/Project_YANDEX)](https://github.com/lk2322/Project_YANDEX/issues)

</div>

---

<p align="center"> Простой мессенджер сделаный в рамках проекта для Яндекс.Лицея
    <br> 
</p>

## 📝 Содержание

- [О проекте](#about)
- [Установка](#getting_started)
- [Использование](#usage)
- [Клиент](client/README.md)
- [TODO](https://trello.com/b/7IAf7cMK)
- [Автор](#authors)
## 🧐 О проекте <a name = "about"></a>

Простой мессенджер, который в свой серверной части использует flask, а в клиентской PyQt5. Имеет функции регистрации и логина(пароли хранятся в виде хешей), умеет создавать беседы между двумя пользователями. Чисто технически может создавать беседы, но для этого нужны правки в API


## 🏁 Установка <a name = "getting_started"></a>
Здесь описывается установка серверной части, для установки клиентской загляните [сюда](client/README.md)
Установите Python 3
```
git clone https://github.com/lk2322/Project_YANDEX
cd Project_YANDEX
pip install -r requirements_server.txt
```
Переименуйте example_env в .env и замените значения HOST_IP и SECRET_KEY на необходимые



## 🎈 Использование <a name="usage"></a>

```
python server.py
```


## ✍️ Автор <a name = "authors"></a>

- [@lk2322](https://github.com/lk2322)
