import re
import time

from paramiko import SSHClient, AutoAddPolicy, AuthenticationException, SSHException
from linux_settings.exceptions import ExecuteCommandException


class SSH:
    def __init__(self, **kwargs):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.kwargs = kwargs

    def __enter__(self):
        try:
            self.client.connect(
                hostname=self.kwargs.get('hostname'),
                port=int(self.kwargs.get('port', 22)),
                username=self.kwargs.get('username'),
                password=self.kwargs.get('password'),
            )
        except AuthenticationException:
            print("Authentication failed, please verify your credentials")
        except SSHException as sshException:
            print(f"Could not establish SSH connection {sshException}")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def execute_cmd(self, cmd, sudo=False, input_data=None, timeout=None):
            if sudo and  self.kwargs.get('username') != 'root':
                cmd = f'sudo -S -p "" {cmd}'
                input_data = self.kwargs.get('password') + '\n'
            stdin, stdout, stderr = self.client.exec_command(cmd, timeout=timeout)
            if input_data is not None:
                stdin.write(input_data)
                stdin.flush()
            output_data = stdout.read()
            output_data = output_data.decode()
            err = stderr.read()
            err = err.decode()
            if err:
                raise ExecuteCommandException(f'Err:{err}')

            return output_data


if __name__ == '__main__':
    with SSH(hostname='192.168.1.15', username='centos', password='centos', port=2002) as ssh:
        commands = [
            'whoami'
        ]

        for command in commands:
            print(ssh.execute_cmd(command))