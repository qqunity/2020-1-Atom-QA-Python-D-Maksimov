import os


def get_vk_api_mock_server_info():
    with open('./project/vk_api_mock_server/config.txt', 'r') as config_file:
        lines = config_file.readlines()
        config = dict()
        for line in lines:
            key = line.split(' = ')[0]
            value = line.split(' = ')[1]
            config[key] = value
        host = os.popen('./project/vk_api_mock_server/get_vk_api_mock_server_host').read().split('\n')[0]
        port = int(config['VK_URL'].split(':')[1])
        return host, port
