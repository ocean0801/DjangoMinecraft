from django.conf.urls import url
from django.test import Client,TestCase
from .models import Config
from django.contrib.auth.models import User
from .urls import urlpatterns
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
    for text in urlpatterns:
      response = client.get("/mine/"+str(text.pattern))
      print(list_print(str(text.pattern),str(response.status_code)))
test = DjagoMinecraftUrlTest()
test.ResponseTest()