# DjnagoMinecraftRcon
 DjangoからMinecraftを制御します。mcipc必須。
    pip3 install mcipc
 でやってください。[公式サイト](https://pypi.org/project/mcipc/) [公式ドキュメント](https://mcipc.readthedocs.io/en/latest/)
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
  権限:スーパーユーザー。
  pass:awajitest
 ### openuser
  権限:なし。
  pass:testtest
 ### Coder
  権限:スタッフ権限。
  pass:testcode
  Codeだけを編集できます。
 ## Toolsフォルダー
 ### port_check.py
 グローバルIPとlocalhostでsocketモジュールで通信してポートをの状況をチェックします。
## 終わりに
 非常にバグが多いです。そして自分のサーバーを動かすためにつくったりしたので、これとMinecraftサーバーを実行するPCを同じにすることを推奨します。
 あと非常に当まわりな実装方法を採用しているため、コードがとても汚いです。
 Minecraftサーバーに人がいないとNoPlayerエラー返ってきますがtry文を書いていないので無視してくだされ。
