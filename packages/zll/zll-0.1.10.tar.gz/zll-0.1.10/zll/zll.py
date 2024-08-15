#!/usr/bin/env python
# encoding=utf-8
# file_name=zll.py

# from __future__ import print_function  # 为了让 Python2 的 print() 不要打印成 tuple
import contextlib
import os
from zbig.zfile import zcsv
from zbig import zprint
from appdirs import user_data_dir
import copy

APP_NAME = "zll"
APP_AUTHOR = "bigzhu"
FILE_NAME = "hosts.csv"
file_path = f"{user_data_dir(APP_NAME, APP_AUTHOR)}{os.sep}{FILE_NAME}"
print(file_path)


# 确保文件建立
def create_file():
    if os.path.exists(file_path):
        return
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write("User,Host,Port,Description\n")
    print(f"Create file: {file_path}")


def read_hosts():
    """
    读取置文件
    """
    header, rows = zcsv.read_csv(file_path)
    print(f"Use ssh connect info file: {file_path}")
    return header, rows


# 添加 number 和打印
def print_info(header: list, rows: list):
    number_header = copy.copy(header)  # copy header
    number_header.insert(0, "Number")
    print_rows = [[i] + rows[i] for i in range(len(rows))]
    zprint.table([number_header] + print_rows, "    ")


def ssh(ssh_info):
    user = ssh_info[0]
    ip = ssh_info[1]
    port = ssh_info[3] if len(ssh_info) > 4 else 22
    print("ssh loging %s ......" % ip)
    command = "export TERM=xterm;ssh -p %s %s@%s" % (port, user, ip)
    os.system(command)


def add_new():
    user = input("Input username:")
    if user is None:
        raise ValueError("Must input username")
    host = input("Input ip or hostname:")
    if host is None:
        raise ValueError("Must input ip or hostname")
    port = input("Input port(default 22):").strip() or 22
    description = input("Input comment:").strip() or ""
    zcsv.write_csv_append(file_path, [user, host, port, description])
    print("Added successfully!")
    main()


def delete_old(s_number):
    i_number = int(s_number)
    zcsv.write_csv_delete(file_path, i_number)
    print("Delete successfully!")
    main()


def select(header: list, rows: list):
    print_info(header, rows)
    # 输入
    i_value = input("input number or ip or hostname (q quit, a add, d delete):")
    if i_value == "":
        select(header, rows)
    if i_value == "a":
        add_new()
        return
    if i_value == "q":
        exit(0)
    if i_value == "d":
        d_value = input("input number to delete):")
        delete_old(d_value)
    with contextlib.suppress(ValueError):
        # 尝试转为int, 看输入是否为编号
        i_value = int(i_value)
        if i_value <= len(rows):
            ssh(rows[i_value])
            return
        else:
            i_value = str(i_value)

    selected_ssh_infos = []
    for i in rows:
        index = i[1].find(i_value)
        if index != -1:
            selected_ssh_infos.append(i)
            continue
        # 搜索描述
        index = i[3].find(i_value)
        if index != -1:
            selected_ssh_infos.append(i)

    if not selected_ssh_infos:
        print("Can't find any IP similar to this one.")
        select(header, rows)
    elif len(selected_ssh_infos) == 1:  # 找到一个，直接登录
        ssh(selected_ssh_infos[0])
        return
    else:
        print(
            "Found %s matching %s, please select again!"
            % (len(selected_ssh_infos), i_value)
        )
        return select(header, selected_ssh_infos)  # 找到一堆，再过滤


def main():
    create_file()
    header, hosts = read_hosts()
    select(header, hosts)


if __name__ == "__main__":
    main()
