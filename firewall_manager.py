import platform
import subprocess
import sys

class FirewallManager:
    def __init__(self):
        self.os_type = platform.system()
        if self.os_type not in ['Windows', 'Linux']:
            raise NotImplementedError("Unsupported OS. This module supports Windows and Linux only.")

    def block_port(self, port):
        if self.os_type == 'Windows':
            self._block_port_windows(port)
        elif self.os_type == 'Linux':
            self._block_port_linux(port)

    def unblock_port(self, port):
        if self.os_type == 'Windows':
            self._unblock_port_windows(port)
        elif self.os_type == 'Linux':
            self._unblock_port_linux(port)

    def _block_port_windows(self, port):
        try:
            subprocess.check_call([
                'netsh', 'advfirewall', 'firewall', 'add', 'rule',
                f'name=Block Port {port}',
                f'dir=in',
                f'protocol=TCP',
                f'localport={port}',
                'action=block'
            ], shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to block port {port} on Windows: {e}")
            raise

    def _unblock_port_windows(self, port):
        try:
            subprocess.check_call([
                'netsh', 'advfirewall', 'firewall', 'delete', 'rule',
                f'name=Block Port {port}',
                f'dir=in',
                f'protocol=TCP',
                f'localport={port}'
            ], shell=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to unblock port {port} on Windows: {e}")
            raise

    def _block_port_linux(self, port):
        try:
            subprocess.check_call(['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', str(port), '-j', 'DROP'])
        except subprocess.CalledProcessError as e:
            print(f"Failed to block port {port} on Linux: {e}")
            raise

    def _unblock_port_linux(self, port):
        try:
            subprocess.check_call(['sudo', 'iptables', '-D', 'INPUT', '-p', 'tcp', '--dport', str(port), '-j', 'DROP'])
        except subprocess.CalledProcessError as e:
            print(f"Failed to unblock port {port} on Linux: {e}")
            raise
