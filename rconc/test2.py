import time
from webob import Request, Response
from mcipc.rcon.je import Biome, Client
#HTMLの記載
html = """
<form method="post">State:
<input type="text" name = "state">
<input type="submit" name="button" value ="Set">
</form>
"""
count = 0
re = ""
class WebApp(object):
    def __call__(self, environ, start_response):
        req = Request(environ)
       # print ('req: %s...' % req.path )
        if req.path == '/':
            command = req.params.get('state', '0')
            print(command)
            if command == "/stop":
                with Client('127.0.0.1', 25575, passwd='minecraft') as client:
                    client.stop()
            resp = Response(html)
        else:
            resp = Response()
                        
        return resp(environ ,start_response)
                        
application = WebApp() 
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = 8080
    httpd = make_server('',port,application)
    print ('serving http port %s...' % port)

    httpd.serve_forever() #serverkidou
