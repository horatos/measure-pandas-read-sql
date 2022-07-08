# 実験のセットアップをする環境とコードを実装する

要件から必要となるのはMySQLとPostgreSQLであるが、これらはDockerで用意する。
さらに実験コードを格納したイメージも必要になる。
これらのイメージをコンテナとして起動するためにdocker composeを利用する。
Compose fileに記述するサービスは以下のとおりである。

- app : 実験コードを実行する。
- mysql : MySQLサーバー。
- postgre : PostgreSQLサーバー。

今回は大きくないプログラムなので、セットアップコードも実験コードもappが保持する。
appのためにDockerfileを作成する。コンテナ内でpipを実行してパッケージをインストールする。

ディレクトリ構成は以下のとおり。

- Dockerfile
- docker-compose.yml
- app
  - requirements.txt
  - main.py
