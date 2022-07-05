# ユーザーストーリーを収集する

まずはユーザーストーリーマッピングを行う。

- 実験のセットアップをする。
  - MySQLコンテナでmysqldが立ち上がるのを待つ。
    - 完全に立ち上がるまでデータを書き込めない。
    - 初期化に時間がかかる。
  - PosgreSQLコンテナでposgresが立ち上がるのを待つ。
  - MySQLコンテナにN件のタプルを書き込む。
  - PosgreSQLコンテナにN件のタプルを書き込む。
- 仮説1を実行する。
  - 以下の手順を実装する関数に`@profile`を付ける。
  - `sqlalchemy.create_engine`で作成した`engine`の`execution_options`は呼び出さ*ない*。
  - `pandas.read_sql("SELECT * FROM table", engine)`を実行してすべての行を読み込む。
  - 読み込んだ行数を印字する。
- 仮説2を実行する。
  - 以下の手順を実装する関数に`@profile`を付ける。
  - `sqlalchemy.create_engine`で作成した`engine`の`execution_options`は呼び出さ*ない*。
  - `pandas.read_sql("SELECT * FROM table", engine, chunksize=CHUNKSIZE)`を実行してすべての行を読み込む。
  - 読み込んだ行数を印字する。
- 仮説3を実行する。
  - 以下の手順を実装する関数に`@profile`を付ける。
  - `sqlalchemy.create_engine`で作成した`engine`の`execution_options`に`stream_results=True`を渡す。
  - `pandas.read_sql("SELECT * FROM table", engine)`を実行してすべての行を読み込む。
  - 読み込んだ行数を印字する。
- 仮説4を実行する。
  - 以下の手順を実装する関数に`@profile`を付ける。
  - `sqlalchemy.create_engine`で作成した`engine`の`execution_options`に`stream_results=True`を渡す。
  - `pandas.read_sql("SELECT * FROM table", engine, chunksize=CHUNKSIZE)`を実行してすべての行を読み込む。
  - 読み込んだ行数を印字する。
