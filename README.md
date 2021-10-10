# DjnagoMinecraftRcon
 DjangoからMinecraftを制御します。mcipc必須。
 ~~~~
 pip3 install mcipc
 ~~~~
 インストールしてください。<br>
 [公式サイト](https://pypi.org/project/mcipc/) 
 [公式ドキュメント](https://mcipc.readthedocs.io/en/latest/)
# 使い方
 ## 環境構築
 kankyou.batでできます。
 ## RunServer
 ~~~~
 py manage.py runserver
 ~~~~
 ## Mig
 ~~~~
 cd shellscripts
 bash mig.sh
 ~~~~
 マイグレーションファイルの作成→適用
# 機能
 ## コンソール @ /mine/console
 /をつけて入力でコマンドを実行します。
 /をつけないとチャットになります。
 
 ###コマンド類
 
 #### /script <id>
 idにかかれたスクリプトの実行。
 #### /query
 サーバーに対してqueryを実行。
 #### /config
 現在のコンフィグを取得。
 ## Query @ /mine/query
 Queryを飛ばします。
 ## Stats @ /mine/stats(近日実装)
 サーバーの統計を出します。
 ## Config @ /mine/config
 サーバーの設定を保存します。
 /mine/configで設定ができます。
 ## スクリプト @ /mine/script
 たくさんのコマンドを一気に実行する機能。
# 終わりに
 非常にバグが多いです。そして自分のサーバーを動かすためにつくったりしたので、これとMinecraftサーバーを実行するPCを同じにすることを推奨します。<br>
 あと非常に遠回りな実装方法を採用しているため、コードがとても汚いです。<br>
