import sys

from mcipc.query import Client as Client_q
from mcipc.rcon.je import Client
import mcipc.rcon.errors
from rcon.exceptions import WrongPassword

import subprocess
from subprocess import PIPE
help = """
#コマンドプロンプトを出す
用法:rcon_c [IP]@[PORT]
#Query飛ばせる
用法:rcon_c [IP]@[PORT] -q
#Help出す
用法:rcon_c -help
"""
ver = "1.1.0"
spaces = 12
def created_commands(com,data):
    pass
def color(name):
    if name == "white" or name == "defuault":
        print('\033[m', end='')
    elif name == "red":
        print('\033[31m', end='')
    elif name == "green":
        print('\033[32m', end='')
    elif name == "blue":
        print('\033[36m', end='')
    elif name == "yellow":
        print('\033[33m', end='')
    elif name == "purple":
        print('\033[35m', end='')
def do(data,passw):
    with Client(data[0], int(data[1]), passwd=passw) as client:
        while True:
            try:
                command = input(">")
            except KeyboardInterrupt:
                print("")
                print(data[0]+"@"+data[1]+"'s RCON client closed.")
                return
            command_list = command.split(' ')
            try:
                if command_list == ['close'] or command_list == ['exit']:
                    print(data[0]+"@"+data[1]+"'s RCON client closed.")
                    return
                if command_list == ['']:
                    continue
                logs = client.run(*command_list)
                if command_list == ['stop']:
                    print('\033[32m'+logs+'\033[m')
                    return
                print(logs)
            except mcipc.rcon.errors.UnknownCommand:
                created_commands(command_list,data)
            except mcipc.rcon.errors.NoPlayerFound:
                print('\033[31m[Error]NoPlayerFound\033[m')
            
def commmandline(datas):
    print("Connecting for "+datas)
    client_data = datas
    data = client_data.split('@')
    passw = input("pass:")
    try:
        do(data,passw)
    except ConnectionRefusedError:
        print('\033[31m[WinError 10061]サーバーに接続できません\033[m')
    except KeyboardInterrupt:
        return
    except ConnectionAbortedError:
        print('\033[31m[WinError 10053]Server Closed\033[m')
    except WrongPassword:
        print('\033[31mThe passward is wrong!\033[m')
        while True:
            passw = input("pass:")
            try:
                with Client(data[0], int(data[1]), passwd=passw) as client:
                    pass
            except WrongPassword:
                print('The passward is wrong!')
            else:
                do(data,passw)
def list_print(list_type,data):
    space = spaces - len(list_type)
    list_type = list_type +( ' ' * space)
    print(list_type+data)
def query():
    client_data = sys.argv[1]
    data = client_data.split('@')
    with Client_q(data[0], int(data[1])) as client:
        full_stats = client.stats(full=True)
    list_print('element','data')
    print('-'*(spaces+len(str(full_stats.host_name))))
    list_print('type',str(full_stats.type))
    list_print('session_id',str(full_stats.session_id))
    list_print('motd',str(full_stats.host_name))
    list_print('game_type',str(full_stats.game_type))
    list_print('game_id',str(full_stats.game_id))
    list_print('version',str(full_stats.version))
    list_print('plugins',str(full_stats.plugins))
    list_print('map',str(full_stats.map))
    list_print('players',str(full_stats.num_players)+'/'+str(full_stats.max_players)+' '+str(full_stats.players))
    list_print('host',str(full_stats.host_ip)+'@'+str(full_stats.host_port))

def help_docs():
    print(help)
def version():
    print("ver:\033[32m"+ver)
    color('white')
    print('Please type for "rcon_c -help" help.')

if len(sys.argv) == 1:
    version()

elif len(sys.argv) == 2: #引数一つ
    if sys.argv[1] == "-h" or sys.argv[1] == "-help":
        help_docs()
    elif sys.argv[1] == "-r" or sys.argv[1] == "-rcon":
        commmandline("localhost@25575")
    else:
        commmandline(sys.argv[1])
elif len(sys.argv) == 3: #引数二つ
    if sys.argv[2] == "-q" or sys.argv[2] == "-query":
        query()

color('white')