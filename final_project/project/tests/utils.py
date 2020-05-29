import os


class Logger:

    def __init__(self, log_writer_path):
        self.log_writer_path = log_writer_path

    def start_logging(self, log_path):
        self.log_path = log_path
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
        os.system(f'touch {self.log_path}')
        os.system(f'{self.log_writer_path} -f {self.log_path}')
        with open(self.log_path, 'r') as log_file:
            self.pre_log_info = log_file.readlines()

    def stop_logging(self):
        if os.path.exists(self.log_path):
            os.remove(self.log_path)
        os.system(f'touch {self.log_path}')
        os.system(f'{self.log_writer_path} -f {self.log_path}')
        with open(self.log_path, 'r') as log_file:
            self.cur_log_info = log_file.readlines()
        os.remove(self.log_path)

    def get_log_info(self):
        log_info = list()
        for line in self.cur_log_info:
            if not line in self.pre_log_info:
                log_info.append(line)
        return ''.join(log_info)
