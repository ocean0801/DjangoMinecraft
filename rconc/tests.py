from logging import exception
from django.test import Client,TestCase
from .models import Config
from django.contrib.auth.models import UserManager , User
from .urls import urlpatterns
from mcipc.rcon.je import Client
from mcipc.query import Client as Client_q
from mcipc.rcon.errors import *
class PageError(Exception):
  "ページのエラーってことだよ。"
def list_print(list_type,data):
    space = 36 - len(list_type)
    list_type = list_type + ' ' * space
    return list_type + data
class DjagoMinecraftUrlTest(TestCase):
  def TestClient(self):
    client = Client()
    response = client.get('/mine/')
    print(response.status_code)
  def ResponseTest(self):
    print("-"*70)
    print("設定されているURL:")
    client = Client()
    list_print("element","num")
    errors = 0
    num = 0
    for text in urlpatterns:
      try:
        num += 1
        response = client.get("/mine/"+str(text.pattern))
      except:
        print(list_print(str(text.pattern),"PageError!"))
        errors += 1
      else:
        print(list_print(str(text.pattern),str(response.status_code)))
    print(str(errors)+"/"+str(num)+"pages is Error!")
  def UserLoginTest(self):
    """
    client = Client()
    testuser = UserManager()
    user = testuser.create_user("testuser","","awaji")
    """
    client = Client()
    user = User("testuser","","awaji")
    client.login(username='testuser', password='awaji')
    print("Login successful!")
  def ConfigTest(self):
    client = Client()
    user = User("testuser","","awaji")
    client.login(username='testuser', password='awaji')
    conf = Config(server_name="test",user=user,server_ip="",rcon_port="25575",query_port="25565",passw="minecraft")
    print("Create conf successful!")
  def ServerTest(self):
    with Client("localhost","25575",passwd="minecraft") as client:
      pass