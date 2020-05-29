FROM python:3.8

ADD /requirements_for_mock_server.txt project/requirements.txt
ADD /mock_server.py project/vk_api_mock_server/mock_server.py
ADD /config.txt project/vk_api_mock_server/config.txt
ADD /mysql_client.py project/vk_api_mock_server/mysql_client.py
ADD /mysql_models.py project/vk_api_mock_server/mysql_models.py

RUN pip3.8 install -r /project/requirements.txt

WORKDIR /project
RUN export PYTHONPATH="${PYTHONPATH}:/project"

EXPOSE 5005

CMD ["python", "./vk_api_mock_server/mock_server.py", "./vk_api_mock_server/config.txt"]