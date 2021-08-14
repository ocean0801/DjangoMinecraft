import socket
print('localhost')
for port in [80,443,8000,8123,25565,25575]:
    try:
        s = socket.socket()
        s.connect(('localhost', port))
        print('オープンされているポート:%d' % port)
        s.close()

    except:
        print('クローズされているポート:%d' % port)
        s.close()
        pass
print('--------')
import requests
res = requests.get('http://inet-ip.info/ip')
g_ip = res.text
print('globalIP('+g_ip+')')
for port in [80,443,8000,8123,25565,25575]:
    try:
        s = socket.socket()
        s.connect((g_ip, port))
        print('オープンされているポート:%d' % port)
        s.close()

    except:
        print('クローズされているポート:%d' % port)
        s.close()
        pass
