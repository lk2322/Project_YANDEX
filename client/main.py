import main_ui
import login_ui
import server_settings_ui
import connect
import sys
import os
import dotenv
import keyring
import typing
from functools import wraps
dotenv.load_dotenv()


def check_hostname():
    HOSTNAME = os.getenv('HOSTNAME')
    return HOSTNAME


class Main():
    def __init__(self):

        # Всякие переменные
        self.last_messages = {}
        self.error_open = False
        self.listWidgets = {}

        self.app = main_ui.QtWidgets.QApplication(sys.argv)
        # Инициализация ui
        self.ui = main_ui.Ui_Form(main_ui.QtWidgets.QWidget())
        self.login_ui = login_ui.Ui_Form(login_ui.QtWidgets.QWidget())
        self.server_ui = server_settings_ui.Ui_Form(
            server_settings_ui.QtWidgets.QWidget())

        # Получение логина и пароля от keyring
        user = keyring.get_password('messenger', 'user')
        password = keyring.get_password('messenger', 'password')

        # Проверка адреса и пароля
        self.HOSTNAME = check_hostname()
        if (not password) or (not check_hostname()):
            self.login_ui.form.show()
        else:
            self.HOSTNAME = check_hostname()
            self._init_main(user, password)

        # closeEvent для  server_ui
        self.server_ui.form.closeEvent = self.closeEvent_s

        # События
        self.login_ui.pushButton.clicked.connect(self.hostname_form)
        self.server_ui.pushButton.clicked.connect(self.add_hostname)
        self.login_ui.register_btn.clicked.connect(self.sign_in_up)
        self.login_ui.login_btn.clicked.connect(self.sign_in_up)
        self.ui.pushButton_2.clicked.connect(self.add_thread)
        self.ui.listWidget.currentItemChanged.connect(self.update_loop)
        self.ui.pushButton.clicked.connect(self.send_message)
        self.ui.pushButton_3.clicked.connect(self.out)
        self.ui.lineEdit.returnPressed.connect(self.send_message)
        self.ui.lineEdit_2.returnPressed.connect(self.add_thread)

        sys.exit(self.app.exec_())

    # Кастомный closeEvent
    def closeEvent_s(self, *args, **kwargs):
        self.login_ui.form.show()
        self.server_ui.form.hide()

    def hostname_form(self):
        self.server_ui.form.show()
        self.login_ui.form.hide()

#   Настройка главного окна(установка соединения)
    def _init_main(self, user: str, password: str):
        self.ui.form.show()
        self.connection = connect.Connect(self.HOSTNAME, user, password)
        try:
            self.connection.get_token()
        except connect.requests.ConnectionError:
            self.error('Не удалось подключиться к серверу')
        self.update_threads()
        # Цикл обновления
        self.timer = main_ui.QtCore.QTimer(self.ui.form)
        self.timer.start(1000)
        self.timer.timeout.connect(self.update_loop)

    def add_hostname(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        open(dotenv_path, 'w').close()
        try:
            connect.requests.get(self.server_ui.lineEdit.text())
        except Exception as e:
            self.error('Ошибка при подключении к серверу', e.__str__())
            return
        dotenv.set_key(dotenv_path, 'HOSTNAME', self.server_ui.lineEdit.text())
        self.HOSTNAME = self.server_ui.lineEdit.text()
        self.server_ui.form.hide()
        self.login_ui.form.show()

    def update_loop(self):
        # Цикл обновления инфы
        try:
            self.update_threads()
            self.get_messages()
        except Exception as e:
            self.timer.stop()
            self.error('Соединение с сервером потеряно', e.__str__())
            sys.exit()

    def out(self):
        keyring.delete_password('messenger', 'user')
        keyring.delete_password('messenger', 'password')
        sys.exit()

    def add_messages_to_list(self, messages: dict):
        """Добавляет сообщения в listwidget

        Args:
            messages (dict): Словарь с сообщениями
            В messages хранятся словари вида
            {message_id (int): {'datetime': int,
                               'text': str,
                               'user_id': int,
                               'username': str}
            }
        """
        for i in messages:
            item = main_ui.QCustomQWidget()
            item.setTextUp(messages[i]['username'])
            if messages[i]['username'] == self.connection.login:
                item.textUpQLabel.setStyleSheet('color: rgb(7,82,1);')
                item.setTextUp('Вы')
            item.setTextDown(messages[i]['text'])
            myQListWidgetItem = main_ui.QtWidgets.QListWidgetItem(
                self.ui.listWidget_2)
            myQListWidgetItem.setSizeHint(item.sizeHint())
            self.ui.listWidget_2.addItem(myQListWidgetItem)
            self.ui.listWidget_2.setItemWidget(myQListWidgetItem, item)

    def get_messages(self):
        scroll = self.save_scroll(self.ui.listWidget_2)
        try:
            thread = self.currentUser
        except AttributeError:
            return
        thr_id = self.threads.get(thread)
        messages = self.connection.get_messages(thr_id)
        if messages == self.last_messages:
            return
        self.last_messages = messages
        # Отключает перерисовку на время обновления
        self.ui.listWidget_2.setUpdatesEnabled(False)

        self.ui.listWidget_2.clear()
        self.add_messages_to_list(messages)
        self.set_scroll(self.ui.listWidget_2, scroll)
        # Включает
        self.ui.listWidget_2.setUpdatesEnabled(True)

    def update_threads(self):
        scroll = self.save_scroll(self.ui.listWidget)
        # Сохраняет  текущий итем
        try:
            self.currentUser = self.ui.listWidget.currentItem().text()
        except AttributeError:
            pass
        # Отключает перерисовку на время обновления
        self.ui.listWidget.setUpdatesEnabled(False)

        self.ui.listWidget.clear()
        self.threads = self.connection.get_threads()
        for i in self.threads:
            self.ui.listWidget.addItem(i)
        self.set_scroll(self.ui.listWidget, scroll)
        # Включает
        self.ui.listWidget.setUpdatesEnabled(True)

    def save_scroll(self, listWidget: main_ui.QtWidgets.QListWidget):
        """Отдаёт позицию скрола

        Args:
            listWidget (main_ui.QtWidgets.QListWidget): [description]
        return:
            int or str
        """
        scroll = listWidget.verticalScrollBar().value()
        if scroll == listWidget.verticalScrollBar().maximum():
            scroll = 'max'
        return scroll

    def set_scroll(self, listWidget: main_ui.QtWidgets.QListWidget, scroll: typing.Union[int, str]):
        """Ставит скрол на своё место

        Args:
            listWidget (main_ui.QtWidgets.QListWidget):
            scroll (typing.Union[int, str]): позиция скрола
        """
        if scroll == 'max':
            listWidget.scrollToBottom()
        else:
            listWidget.verticalScrollBar().setValue(scroll)

    def send_message(self):
        thr_id = self.threads.get(self.currentUser)
        text = self.ui.lineEdit.text()
        if not text:
            return
        self.connection.send_message(thr_id, text)

        self.get_messages()
        self.ui.lineEdit.clear()

    def add_thread(self):
        user = self.ui.lineEdit_2.text()
        if not user:
            return
        for i in range(self.ui.listWidget.count()):
            if self.ui.listWidget.item(i).text() == user:
                self.error('Текущий пользователь существует')
                return
        # Проверка на добавление самого себя
        if user == self.connection.login:
            return
        try:
            self.connection.new_thread(user)
        except connect.requests.exceptions.ConnectionError as e:
            self.error('Пользователь не найден!', e.__str__())
            return
        self.update_threads()
        self.ui.lineEdit_2.clear()

    def error(self, text: str, e=''):
        """error window

        Args:
            text (str): text error
            e (str, optional): additional information about the error. Defaults to ''.
        """
        error_dialog = main_ui.QtWidgets.QMessageBox()
        error_dialog.setWindowTitle('Ошибка')
        error_dialog.setText(text)
        error_dialog.setDetailedText(e)
        error_dialog.exec_()

    def sign_in_up(self):
        """Функция для регистрации или входа"""
        login = self.login_ui.login_login.text()
        password = self.login_ui.login_pass.text()
        self.connection = connect.Connect(self.HOSTNAME, login, password)
        if not self.HOSTNAME:
            self.error('Настройте адрес сервера')
            return
        try:
            if self.login_ui.form.sender().objectName() == 'login_btn':
                self.connection.get_token()
            else:
                self.connection.register()
        except connect.requests.ConnectionError or connect.requests.exceptions.MissingSchema as e:
            self.error('Ошибка', e.__str__())
            return
        self._login(password, login)

    def _login(self, password: str, login: str):
        self.login_ui.form.hide()
        keyring.set_password('messenger', 'password', password)
        keyring.set_password('messenger', 'user', login)
        self.ui.form.show()
        self._init_main(login, password)


if __name__ == "__main__":
    Main()
