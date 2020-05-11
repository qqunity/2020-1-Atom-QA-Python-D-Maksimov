import pytest
import requests

from linux_settings.remote_control.remote_connection import SSH


@pytest.mark.REMOTEMACHINE
class TestRemoteMachine:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, ssh_connector):
        self.ssh: SSH = ssh_connector

    def test_get_root_permeation(self):
        assert self.ssh.execute_cmd('cat /var/log/messages', sudo=True)

    def test_nginx_ssh(self):
        response_data = self.ssh.execute_cmd('systemctl status nginx', sudo=True).split('\n')
        active_information = ''
        for line in response_data:
            if 'Active' in line:
                active_information = line
        active_information = active_information.split()[1]
        response_data = self.ssh.execute_cmd('netstat -tupln | grep nginx', sudo=True)
        port_information = '2020' in list(map(lambda x: x.split(), response_data.split('\n')))[0][3]
        assert active_information == 'active' and port_information

    def test_nginx_http_correct(self):
        correct_response = requests.get('http://192.168.1.15:2020/')
        assert 'Nginx HTTP Server' in correct_response.text

    def test_nginx_http_incorrect(self):
        with pytest.raises(requests.exceptions.ConnectionError):
            requests.get('http://192.168.1.15:80/')

    def test_nginx_request(self):
        prev_cnt_lines = int(self.ssh.execute_cmd('cat /var/log/nginx/access.log | wc -l', sudo=True))
        requests.delete('http://192.168.1.15:2020/')
        response_data = self.ssh.execute_cmd('cat /var/log/nginx/access.log | tail -n 1', sudo=True)
        cur_cnt_lines = int(self.ssh.execute_cmd('cat /var/log/nginx/access.log | wc -l', sudo=True))
        request_method = response_data.split()[5][1:]
        assert request_method == 'DELETE' and cur_cnt_lines - prev_cnt_lines > 0

    def test_nginx_block(self):
        initial_connection = True
        try:
            requests.get('http://192.168.1.15:2020/')
        except requests.exceptions.ConnectionError:
            initial_connection = False
        self.ssh.execute_cmd('firewall-cmd --remove-port 2020/tcp', sudo=True)
        self.ssh.execute_cmd('systemctl restart nginx', sudo=True)
        end_connection = True
        try:
            requests.get('http://192.168.1.15:2020/')
        except requests.exceptions.ConnectionError:
            end_connection = False
        response_data = self.ssh.execute_cmd('systemctl status nginx', sudo=True).split('\n')
        active_information = ''
        for line in response_data:
            if 'Active' in line:
                active_information = line
        active_information = active_information.split()[1]
        test_res = not end_connection and active_information == 'active' and initial_connection
        self.ssh.execute_cmd('firewall-cmd --reload', sudo=True)
        self.ssh.execute_cmd('systemctl restart nginx', sudo=True)
        assert test_res
