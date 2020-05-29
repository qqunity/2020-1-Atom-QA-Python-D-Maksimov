import os
import time


def wait(func, timeout):
    entry_time = time.time()
    result = None
    while time.time() - entry_time <= timeout:
        result = func()
    return result


def get_selenoid_host():
    return os.popen('/media/qunity/Workspace/Python_projects/qa-project/project/selenoid/get_selenoid_host').read().split('\n')[0]
