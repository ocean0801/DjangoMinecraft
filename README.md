# DjnagoMinecraftRcon
 DjangoからMinecraftを制御します。mcipc必須。
 ~~~~
    pip3 install mcipc
 ~~~~
 インストールしてください。<br>[公式サイト](https://pypi.org/project/mcipc/) [公式ドキュメント](https://mcipc.readthedocs.io/en/latest/)

# 使い方
 run.shを起動してください。
## Models
### Code
 Codeは2個を上限に作成できます。
 常駐します。設定を管理画面からActive・Inactiveにしてから/mine/codeのページで適用してくさださい。
### Config
 サーバーの設定を保存します。
 今はAdminとopenuserが持っています。
 これを設定しないと/mine/com下のものが使えません。
## SampleUserたち
 プロジェクトの過程で三つのユーザーができました。
 ### Admin
  権限:スーパーユーザー。<br>
  pass:awajitest
 ### openuser
  権限:なし。<br>
  pass:testtest
 ### Coder
  権限:スタッフ権限。<br>
  pass:testcode<br>
  Codeだけを編集できます。
 ## Toolsフォルダー
 ### port_check.py
 グローバルIPとlocalhostでsocketモジュールで通信してポートをの状況をチェックします。
 ## ShellScripts
 ### run.sh
 サーバーの実行。
 ### migrun.sh
 マイグレーションファイルの作成→適用→サーバーの実行。
 ### mig.sh
 マイグレーションファイルの作成→適用
 ### codes.sh
 codeの常駐ファイルの実行。(codesを使うときは必須。)
 ### all.sh
 マイグレーションファイルの作成→適用→サーバーの実行&codeの常駐ファイルの実行。
 ### serverall.sh
 マイグレーションファイルの作成→適用→サーバーの実行&codeの常駐ファイルの実行&このサーバーと同じフォルダのserverフォルダにあるserver.jarを
 メモリ4Gを割り当てて起動。<br>
 serverフォルダの下にtemplatesフォルダを置いてください。
 ## filetree
 参考までに。<br>
~~~~
DjangoMinecraft<br>
-LICENSE<br>
-README.md<br>
-\_\_pycache__<br>
-code1.py<br>
-code2.py<br>
-code2.txt<br>
-db.sqlite3<br>
-log.txt<br>
-manage.py<br>
-mysite<br>
-rconc<br>
-shellscripts<br>
-templates<br>
-tools<br>
server<br>
(略)
-ops.json<br>
-permissions.yml<br>
-plugins<br>
-server.jar<br>
-server.properties<br>
-spigot.yml<br>
-templates⇦これ<br>
(略)
~~~~
## 終わりに
 非常にバグが多いです。そして自分のサーバーを動かすためにつくったりしたので、これとMinecraftサーバーを実行するPCを同じにすることを推奨します。
 あと非常に当まわりな実装方法を採用しているため、コードがとても汚いです。
 ~~Minecraftサーバーに人がいないとNoPlayerエラー返ってきますがtry文を書いていないので無視してくだされ。~~
 なくなりました。
