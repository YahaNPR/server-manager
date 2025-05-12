# ssh_handler.py
import paramiko

class SSHHandler:
    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connected = False

    def connect(self):
        try:
            self.client.connect(
                hostname=self.ip,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=5
            )
            self.connected = True
            return True
        except Exception as e:
            return f"Ошибка подключения: {e}"

    def execute_command(self, command):
        if not self.connected:
            return "", "Не подключено к серверу"
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()
        except Exception as e:
            return "", f"Ошибка выполнения: {e}"

    def close(self):
        self.client.close()
        self.connected = False