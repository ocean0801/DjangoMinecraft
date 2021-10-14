from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Script(models.Model):
    script_name = models.CharField("スクリプトの名前",max_length=200)
    script = models.TextField("スクリプトを記述")
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

class Command_log(models.Model):
    command_text = models.CharField("実行したコマンド",max_length=100)
    return_text = models.TextField("実行結果",max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True,null=True)
    q_flag = models.BooleanField(verbose_name="",default=False)
    chat_flag = models.BooleanField(verbose_name="",default=False)
    def __str__(self):
        return self.command_text

class Code(models.Model):
    name = models.CharField("名前",max_length=20,default=None)
    code = models.TextField("コード",max_length=1000)
    def __str__(self):
        return self.name