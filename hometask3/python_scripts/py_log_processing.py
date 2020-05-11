import argparse
import os
import numpy as np
import json

from collections import Counter

from python_scripts.exceptions import ParamsParseException, CommandNotFoundException


def params_parse(params: str):
    if params is not None:
        if params.find('/') == -1:
            raise ParamsParseException("Invalid params format!")
        raw_params = list(map(lambda p: p.split(':'), params.split('/')))
        d_params = dict()
        for param in raw_params:
            if param[0] != '':
                d_params[param[0]] = param[1]
        return d_params


def log_processing(log_path, cmd, output_path=None, params=None):
    if not os.path.isdir(log_path):
        with open(log_path, 'r') as log_file:
            if cmd == 1:
                if output_path is None:
                    print(f'{sum(1 for line in log_file)} lines in {log_path}')
                else:
                    with open(output_path, 'w') as output_file:
                        if output_path.split('.')[-1] == 'json':
                            json.dump({'cmd1': f'{sum(1 for line in log_file)} lines in {log_path}'}, output_file)
                        else:
                            output_file.write(f'{sum(1 for line in log_file)} lines in {log_path}\n')

            elif cmd == 2:
                if output_path is None:
                    print(
                        f'Count of {params["req_type"]} requests is equal {sum(1 for line in log_file if line.find(params["req_type"]) != -1)}')
                else:
                    with open(output_path, 'w') as output_file:
                        if output_path.split('.')[-1] == 'json':
                            json.dump({'cmd2': f'Count of {params["req_type"]} requests is equal {sum(1 for line in log_file if line.find(params["req_type"]) != -1)}'}, output_file)
                        else:
                            output_file.write(
                                f'Count of {params["req_type"]} requests is equal {sum(1 for line in log_file if line.find(params["req_type"]) != -1)}\n')
            elif cmd == 3:
                lines = log_file.readlines()
                lines.sort(key=lambda line: int(line.split()[9]))
                lines.reverse()
                if output_path is None:
                    for i in range(int(params['limit'])):
                        print(lines[i].split()[0] + ' ' + ' '.join(lines[i].split()[6:8]) + ' ' + ' '.join(lines[i].split()[8:10]))
                else:
                    with open(output_path, 'w') as output_file:
                        if output_path.split('.')[-1] == 'json':
                            res = dict()
                            for i in range(int(params['limit'])):
                                res[i] = lines[i].split()[0] + ' ' + ' '.join(lines[i].split()[6:8]) + ' ' + ' '.join(lines[i].split()[8:10])
                            json.dump({'cmd3': res}, output_file)
                        else:
                            for i in range(int(params['limit'])):
                                output_file.write(
                                    lines[i].split()[0] + ' ' + ' '.join(lines[i].split()[6:8]) + ' ' + ' '.join(lines[i].split()[8:10]) + '\n')
            elif cmd == 4:
                lines = log_file.readlines()
                lines = list(map(lambda line: line.replace(line, line.split()[6] + ' ' + line.split()[8]), lines))
                lines = list(filter(lambda line: line.split()[1][0] == '4', lines))
                c_lines = Counter(lines)
                c_lines = list(dict(c_lines).items())
                c_lines.sort(key=lambda item: item[1], reverse=True)
                if output_path is None:
                    for line in c_lines:
                        print(f'{line[0]} is repeated {line[1]} times')
                else:
                    with open(output_path, 'w') as output_file:
                        if output_path.split('.')[-1] == 'json':
                            res = dict()
                            i = 0
                            for line in c_lines:
                                res[i] = f'{line[0]} is repeated {line[1]} times'
                                i += 1
                            json.dump({'cmd4': res}, output_file)
                        else:
                            for line in c_lines:
                                output_file.write(f'{line[0]} is repeated {line[1]} times\n')
            elif cmd == 5:
                lines = log_file.readlines()
                lines = list(map(lambda line: line.replace(line, line.split()[0] + ' ' + line.split()[6] + ' ' + line.split()[8] + ' ' + line.split()[9]), lines))
                lines = list(filter(lambda line: line.split()[2][0] == '4', lines))
                lines = list(np.unique(np.array(lines)))
                lines.sort(key=lambda line: int(line.split()[3]), reverse=True)
                if output_path is None:
                    for i in range(int(params['limit'])):
                        print(lines[i])
                else:
                    with open(output_path, 'w') as output_file:
                        if output_path.split('.')[-1] == 'json':
                            res = dict()
                            for i in range(int(params['limit'])):
                                res[i] = lines[i]
                            json.dump({'cmd5': res}, output_file)
                        else:
                            for i in range(int(params['limit'])):
                                output_file.write(lines[i] + '\n')
            else:
                raise CommandNotFoundException("Command not found!")
    else:
        if os.path.exists(output_path):
            os.remove(output_path)
        for log_file_path in os.listdir(log_path):
            if output_path is None:
                print('-' * 50)
                print(log_file_path)
                print('-' * 50)
            else:
                if output_path.split('.')[-1] != 'json':
                    with open(output_path, 'a') as output_file:
                        output_file.write('-' * 50 + '\n' + log_file_path + '\n' + '-' * 50 + '\n')
            with open(os.path.join(log_path, log_file_path), 'r') as log_file:
                if cmd == 1:
                    if output_path is None:
                        print(f'{sum(1 for line in log_file)} lines in {log_path}')
                    else:
                        with open(output_path, 'a') as output_file:
                            if output_path.split('.')[-1] == 'json':
                                json.dump({'cmd1': f'{sum(1 for line in log_file)} lines in {log_path}'}, output_file)
                            else:
                                output_file.write(f'{sum(1 for line in log_file)} lines in {log_path}\n')

                elif cmd == 2:
                    if output_path is None:
                        print(
                            f'Count of {params["req_type"]} requests is equal {sum(1 for line in log_file if line.find(params["req_type"]) != -1)}')
                    else:
                        with open(output_path, 'a') as output_file:
                            if output_path.split('.')[-1] == 'json':
                                json.dump({'cmd2': f'Count of {params["req_type"]} requests is equal {sum(1 for line in log_file if line.find(params["req_type"]) != -1)}'}, output_file)
                            else:
                                output_file.write(f'Count of {params["req_type"]} requests is equal {sum(1 for line in log_file if line.find(params["req_type"]) != -1)}\n')
                elif cmd == 3:
                    lines = log_file.readlines()
                    lines.sort(key=lambda line: int(line.split()[9]))
                    lines.reverse()
                    if output_path is None:
                        for i in range(int(params['limit'])):
                            print(lines[i].split()[0] + ' ' + ' '.join(lines[i].split()[6:8]) + ' ' + ' '.join(
                                lines[i].split()[8:10]))
                    else:
                        with open(output_path, 'a') as output_file:
                            if output_path.split('.')[-1] == 'json':
                                res = dict()
                                for i in range(int(params['limit'])):
                                    res[i] = lines[i].split()[0] + ' ' + ' '.join(
                                        lines[i].split()[6:8]) + ' ' + ' '.join(lines[i].split()[8:10])
                                json.dump({'cmd3': res}, output_file)
                            else:
                                for i in range(int(params['limit'])):
                                    output_file.write(
                                        lines[i].split()[0] + ' ' + ' '.join(lines[i].split()[6:8]) + ' ' + ' '.join(lines[i].split()[8:10]) + '\n')
                elif cmd == 4:
                    lines = log_file.readlines()
                    lines = list(map(lambda line: line.replace(line, line.split()[6] + ' ' + line.split()[8]), lines))
                    lines = list(filter(lambda line: line.split()[1][0] == '4', lines))
                    c_lines = Counter(lines)
                    c_lines = list(dict(c_lines).items())
                    c_lines.sort(key=lambda item: item[1], reverse=True)
                    if output_path is None:
                        for line in c_lines:
                            print(f'{line[0]} is repeated {line[1]} times')
                    else:
                        with open(output_path, 'a') as output_file:
                            if output_path.split('.')[-1] == 'json':
                                res = dict()
                                i = 0
                                for line in c_lines:
                                    res[i] = f'{line[0]} is repeated {line[1]} times'
                                    i += 1
                                json.dump({'cmd4': res}, output_file)
                            else:
                                for line in c_lines:
                                    output_file.write(f'{line[0]} is repeated {line[1]} times\n')
                elif cmd == 5:
                    lines = log_file.readlines()
                    lines = list(map(lambda line: line.replace(line, line.split()[0] + ' ' + line.split()[6] + ' ' + line.split()[8] + ' ' + line.split()[9]), lines))
                    lines = list(filter(lambda line: line.split()[2][0] == '4', lines))
                    lines = list(np.unique(np.array(lines)))
                    lines.sort(key=lambda line: int(line.split()[3]), reverse=True)
                    if output_path is None:
                        for i in range(int(params['limit'])):
                            print(lines[i])
                    else:
                        with open(output_path, 'a') as output_file:
                            if output_path.split('.')[-1] == 'json':
                                res = dict()
                                for i in range(int(params['limit'])):
                                    res[i] = lines[i]
                                json.dump({'cmd5': res}, output_file)
                            else:
                                for i in range(int(params['limit'])):
                                    output_file.write(lines[i] + '\n')
                else:
                    raise CommandNotFoundException("Command not found!")
                if output_path is None:
                    print('*' * 50)
                else:
                    if output_path.split('.')[-1] != 'json':
                        with open(output_path, 'a') as output_file:
                            output_file.write('*' * 50 + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_path', type=str, dest='log_path')
    parser.add_argument('--cmd', type=int, dest='cmd')
    parser.add_argument('--params', type=str, dest='params')
    parser.add_argument('--output_path', type=str, dest='output')

    args = parser.parse_args()

    log_processing(args.log_path, args.cmd, output_path=args.output, params=params_parse(args.params))
