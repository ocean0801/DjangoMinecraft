# DjnagoMinecraftRcon
 DjangoからMinecraftを制御します。mcipc必須。
 ~~~~
 pip3 install mcipc
 ~~~~
 インストールしてください。<br>[公式サイト](https://pypi.org/project/mcipc/) [公式ドキュメント](https://mcipc.readthedocs.io/en/latest/)

# 使い方
 ## RunServer
 ~~~~
 cd DjangoMinecraft
 py manage.py runserver
 ~~~~
 ## Mig
 ~~~~
 cd shellscripts
 bash mig.sh
 ~~~~
 マイグレーションファイルの作成→適用
## Models
### Code
 Codeは2個を上限に作成できます。
 常駐します。設定を管理画面からActive・Inactiveにしてから/mine/codeのページで適用してくさださい。
### Config
 サーバーの設定を保存します。
 これを設定しないと/mine/com下のものが使えません。
 /mine/configで設定ができますがパスワードの設定方法については模索しています。
 ## Toolsフォルダー
 ### port_check.py
 グローバルIPとlocalhostでsocketモジュールで通信してポートをの状況をチェックします。
 requestsモジュール必須。
 ~~~~
 pip install requests
 ~~~~
 でインストールしてください。
## 終わりに
 非常にバグが多いです。そして自分のサーバーを動かすためにつくったりしたので、これとMinecraftサーバーを実行するPCを同じにすることを推奨します。<br>
 あと非常に遠回りな実装方法を採用しているため、コードがとても汚いです。<br>
