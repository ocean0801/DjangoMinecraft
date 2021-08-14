from mcipc.rcon.je import Client
import time
function = ""
ip = "127.0.0.1"
port = 25575
re = ""
sleeptime = 1
while True:
    with open("code2.txt","r",encoding="UTF-8") as f:
        lines = f.readlines()
        sleeptime = float(lines[2])
    if lines[0] == "1\n":
        #print("t")
        function = lines[1]
        funcs_list = function.split("/")
        function = funcs_list[1]
        func_du = function.split(" ")
        func_du[-1] = func_du[-1].split("\n")
        func_du[-1] = func_du[-1][0]
        with Client(ip, port, passwd='minecraft') as client:
            re = client.run(*func_du)
    '''print(funcs_list)
    print(lines)'''
    #print(func_du)
    '''print(lines[1])'''
    time.sleep(sleeptime)
    #print(sleeptime) #debug
