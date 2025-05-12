# main.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget,
    QTextEdit, QLabel, QMessageBox, QLineEdit
)

# Импортируем модули
from server_data import SERVERS
from ssh_handler import SSHHandler
from package_manager import PackageManager

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Менеджер серверов")
        self.resize(600, 400)
        self.layout = QVBoxLayout()

        # Список серверов
        self.server_list = QListWidget()
        self.server_list.addItems([s["name"] for s in SERVERS])
        self.layout.addWidget(QLabel("Выберите сервер:"))
        self.layout.addWidget(self.server_list)

        # Кнопка подключения
        self.connect_btn = QPushButton("Подключиться")
        self.connect_btn.clicked.connect(self.connect_to_server)  # <-- Здесь ссылка на метод
        self.layout.addWidget(self.connect_btn)

        # Поле для установки пакета
        self.package_input = QLineEdit()
        self.install_btn = QPushButton("Установить пакет")
        self.install_btn.clicked.connect(self.install_package)
        self.layout.addWidget(QLabel("Введите имя пакета:"))
        self.layout.addWidget(self.package_input)
        self.layout.addWidget(self.install_btn)

        # Кнопка проверки статуса
        self.check_status_btn = QPushButton("Проверить статус")
        self.check_status_btn.clicked.connect(self.check_service_status)
        self.layout.addWidget(self.check_status_btn)

        # Лог действий
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.layout.addWidget(QLabel("Лог:"))
        self.layout.addWidget(self.log)

        self.setLayout(self.layout)
        self.ssh = None

    def connect_to_server(self):  # <-- Этот метод должен быть здесь
        selected = self.server_list.currentItem()
        if not selected:
            self.show_error("Выберите сервер!")
            return

        server_info = next((s for s in SERVERS if s["name"] == selected.text()), None)
        if not server_info:
            self.show_error("Сервер не найден!")
            return

        self.log.append(f"Подключение к {selected.text()}...")

        # Убираем 'name' перед передачей в SSHHandler
        ssh_data = {k: v for k, v in server_info.items() if k != 'name'}
        self.ssh = SSHHandler(**ssh_data)

        result = self.ssh.connect()
        if result is True:
            self.log.append("✅ Подключено!")
        else:
            self.log.append(f"❌ Ошибка подключения: {result}")

    def install_package(self):
        if not self.ssh or not self.ssh.connected:
            self.show_error("Сначала подключитесь к серверу!")
            return

        package_name = self.package_input.text().strip()
        if not package_name:
            self.show_error("Введите имя пакета!")
            return

        self.log.append(f"⏳ Установка пакета '{package_name}'...")
        pm = PackageManager(self.ssh)
        result = pm.install_package(package_name)
        self.log.append(f"Результат:\n{result}")

    def check_service_status(self):
        if not self.ssh or not self.ssh.connected:
            self.show_error("Сначала подключитесь к серверу!")
            return

        package_name = self.package_input.text().strip()
        if not package_name:
            self.show_error("Введите имя пакета!")
            return

        self.log.append(f"⏳ Проверка статуса {package_name}...")
        pm = PackageManager(self.ssh)
        result = pm.check_service_status(package_name)
        self.log.append(f"Статус:\n{result}")

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())