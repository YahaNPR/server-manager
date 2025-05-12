# package_manager.py
class PackageManager:
    def __init__(self, ssh_handler):
        self.ssh = ssh_handler
        self.os_type = self._detect_os()

    def _detect_os(self):
        stdout, _ = self.ssh.execute_command("cat /etc/os-release")
        if "ubuntu" in stdout.lower() or "debian" in stdout.lower():
            return "ubuntu"
        elif "centos" in stdout.lower() or "rhel" in stdout.lower():
            return "centos"
        else:
            return "unknown"

    def install_package(self, package_name):
        if self.os_type == "ubuntu":
            cmd = f"sudo apt update && sudo apt install -y {package_name}"
        elif self.os_type == "centos":
            cmd = f"sudo yum install -y {package_name}"
        else:
            return "Неизвестный дистрибутив"
        stdout, stderr = self.ssh.execute_command(cmd)
        return stdout + stderr
    
    def check_service_status(self, service_name):
        stdout, stderr = self.ssh.execute_command(f"systemctl status {service_name}")
        return stdout + stderr
    
    def remove_package(self, package_name):
        if self.os_type == "ubuntu":
            cmd = f"sudo apt remove -y {package_name}"
        elif self.os_type == "centos":
            cmd = f"sudo yum remove -y {package_name}"
        stdout, stderr = self.ssh.execute_command(cmd)
        return stdout + stderr