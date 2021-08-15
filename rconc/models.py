from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Script(models.Model):
    script_name = models.CharField("スクリプトの名前",max_length=200)
    script = models.TextField("スクリプトを記述")
    def __str__(self):
        return self.script_name

class Code(models.Model):
    choise_ = (
        ("1","Active"),
        ("2","Inactive"),
    )
    script_name = models.CharField("コードの名前",max_length=200)
    selecter = models.CharField("状態",max_length=1,choices=choise_,default="2")
    condition = models.CharField("実行間隔",max_length=10,default="1")
    code = models.TextField("コード")
    def __str__(self):
        return self.script_name

class Config(models.Model):
    server_name = models.CharField("サーバーの名前",max_length=20,default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    server_ip = models.CharField("サーバーのIPアドレス",max_length=20)
    rcon_port = models.CharField("RCONクライアントのポート番号",max_length=6)
    query_port = models.CharField("Queryクライアントのポート番号",max_length=6)
    passw = models.CharField("パスワード",max_length=200)
    def __str__(self):
        return self.server_name

class Profile(models.Model):
    profile_name = models.CharField("プロファイルの名前",max_length=20,default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    server_ip = models.CharField("サーバーのIPアドレス",max_length=20)
    rcon_port = models.CharField("RCONクライアントのポート番号",max_length=6)
    query_port = models.CharField("Queryクライアントのポート番号",max_length=6)
    passw = models.CharField("パスワード",max_length=200,default=None)
    rq = (
        ("1","Rcon"),
        ("2","Query"),
    )
    rq = models.CharField("Rcon/Query",max_length=10,choices=rq,default="1")
    script = models.TextField(blank=True)
    def __str__(self):
        return self.profile_name
class Command_log(models.Model):
    command_text = models.CharField("実行したコマンド",max_length=100)
    return_text = models.CharField("実行結果",max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.command_text