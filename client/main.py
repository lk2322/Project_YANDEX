import main_ui
import login_ui
import server_settings_ui
import connect
import sys
import os
import dotenv
import keyring
dotenv.load_dotenv()


def check_hostname():
    HOSTNAME = os.getenv('HOSTNAME')
    return HOSTNAME


class Main():
    def __init__(self):
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

        self.login_ui.pushButton.clicked.connect(self.server_ui.form.show)
        self.login_ui.pushButton_2.clicked.connect(self.server_ui.form.show)
        self.server_ui.pushButton.clicked.connect(self.add_hostname)
        self.login_ui.register_btn.clicked.connect(self.sign_up)
        self.login_ui.login_btn.clicked.connect(self.sign_in)
        self.ui.pushButton_2.clicked.connect(self.add_thread)
        self.ui.listWidget.currentItemChanged.connect(self.update_loop)
        self.ui.pushButton.clicked.connect(self.send_message)
        self.ui.pushButton_3.clicked.connect(self.out)
        self.ui.lineEdit.editingFinished.connect(self.send_message)
        self.ui.lineEdit_2.editingFinished.connect(self.add_thread)

        sys.exit(self.app.exec_())
#   Настройка главного окна(установка соединения)

    def _init_main(self, user, password):
        self.ui.form.show()
        self.connection = connect.Connect(self.HOSTNAME, user, password)
        try:
            self.connection.get_token()
        except connect.requests.ConnectionError:
            self.error('Не удалось подключиться к серверу')
        self.update_threads()
        self.timer = main_ui.QtCore.QTimer(self.ui.form)
        self.timer.start(1000)
        self.timer.timeout.connect(self.update_loop)

    def add_hostname(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        open(dotenv_path, 'w').close()
        dotenv.set_key(dotenv_path, 'HOSTNAME', self.server_ui.lineEdit.text())
        self.HOSTNAME = self.server_ui.lineEdit.text()
        self.server_ui.form.hide()

    def update_loop(self):

        self.update_threads()
        self.get_messages()

    def out(self):
        keyring.delete_password('messenger', 'user')
        keyring.delete_password('messenger', 'password')
        sys.exit()

    def get_messages(self):
        # TODO Сделать рефакторинг
        scrol = self.ui.listWidget_2.verticalScrollBar().value()
        if scrol == self.ui.listWidget_2.verticalScrollBar().maximum():
            scrol += 1
        try:
            thread = self.currentUser
        except AttributeError:
            return
        thr_id = self.threads.get(thread)
        messages = self.connection.get_messages(thr_id).json()
        self.ui.listWidget_2.clear()
        for i in messages:
            item = main_ui.QCustomQWidget()
            item.setTextUp(messages[i]['username'])
            if messages[i]['username'] == self.connection.login:
                item.textUpQLabel.setStyleSheet('color: rgb(255, 0, 0);')
            item.setTextDown(messages[i]['text'])
            myQListWidgetItem = main_ui.QtWidgets.QListWidgetItem(
                self.ui.listWidget_2)
            myQListWidgetItem.setSizeHint(item.sizeHint())
            self.ui.listWidget_2.addItem(myQListWidgetItem)
            self.ui.listWidget_2.setItemWidget(myQListWidgetItem, item)
        self.ui.listWidget_2.repaint()
        self.ui.listWidget_2.verticalScrollBar().setValue(scrol)

    def send_message(self):
        thr_id = self.threads.get(self.currentUser)
        text = self.ui.lineEdit.text()
        if not text:
            return
        self.connection.send_message(thr_id, text)

        self.get_messages()
        self.ui.lineEdit.clear()

    def update_threads(self):
        scrol = self.ui.listWidget.verticalScrollBar().value()
        if scrol == self.ui.listWidget.verticalScrollBar().maximum():
            scrol += 1
        # Сохраняет  текущий итем
        try:
            self.currentUser = self.ui.listWidget.currentItem().text()
        except AttributeError:
            pass
        self.ui.listWidget.clear()
        self.threads = self.connection.get_threads().json()
        for i in self.threads:
            self.ui.listWidget.addItem(i)
        self.ui.listWidget.repaint()
        self.ui.listWidget.verticalScrollBar().setValue(scrol)

    def add_thread(self):
        user = self.ui.lineEdit_2.text()
        if not user:
            return
        for i in range(self.ui.listWidget.count()):
            if self.ui.listWidget.item(i).text() == user:
                self.error('Текущий пользователь существует')
                return
        if user == self.connection.login:
            return
        try:
            self.connection.new_thread(user)
        except connect.requests.exceptions.ConnectionError as e:
            self.error('Пользователь не найден!', e.__str__())
        self.update_threads()
        self.ui.lineEdit_2.clear()

    def error(self, text, e=''):
        error_dialog = main_ui.QtWidgets.QMessageBox()
        error_dialog.setWindowTitle('Ошибка')
        error_dialog.setText(text)
        error_dialog.setDetailedText(e)
        error_dialog.exec_()
# TODO Передать отоброжение ошибок через self.error()

    def sign_up(self):
        self.login_ui.register_err.setText('')
        login = self.login_ui.reg_login.text()
        password = self.login_ui.register_pass.text()
        if not self.HOSTNAME:
            self.error('Настройте адрес сервера')
            return
        self.connection = connect.Connect(self.HOSTNAME, login, password)
        try:
            self.connection.register()
        except connect.requests.ConnectionError:
            self.login_ui.register_err.setText('Error')
            return
        self._login(password, login)

    def sign_in(self):
        self.login_ui.login_err.setText('')
        login = self.login_ui.login_login.text()
        password = self.login_ui.login_pass.text()
        self.connection = connect.Connect(self.HOSTNAME, login, password)
        if not self.HOSTNAME:
            self.error('Настройте адрес сервера')
            return
        try:
            self.connection.get_token()
        except connect.requests.ConnectionError:
            self.login_ui.login_err.setText('Error')
            return
        self._login(password, login)

    def _login(self, password, login):
        self.login_ui.form.hide()
        keyring.set_password('messenger', 'password', password)
        keyring.set_password('messenger', 'user', login)
        self.ui.form.show()
        self._init_main(login, password)


if __name__ == "__main__":
    Main()
