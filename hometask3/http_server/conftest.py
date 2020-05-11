import time

import pytest

from http_server.http_client.socket_client import HttpClient
from http_server.mock_server.mock import MockServer


@pytest.fixture(scope='session')
def network_interaction():
    mock = MockServer('127.0.0.1', 5000,
                      data={'users': {
                          '1': {'name': 'Denis', 'surname': 'Maksimov'},
                          '2': {'name': 'Petya', 'surname': 'Ivanov'}
                      }
                      })
    mock.run_mock()
    time.sleep(1)
    client = HttpClient('127.0.0.1', 5000)
    yield mock, client
    mock.shutdown_mock()
