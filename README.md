# `pandas.DataFrame.read_sql`が使用するメモリサイズを測定する

このリポジトリにはPythonのライブラリであるpandasの`DataFrame.read_sql`メソッドが使用するメモリのサイズをいくつかの条件で測定するプログラムがある。
測定に使うRDBMSはMySQLとPostgreSQLの2つ、SQLAlchemyの`stream_results`フラグの値が`True`と`False`の2つの場合、`read_sql`の`chunksize`引数を渡す場合と渡さない場合の2つにについて測定を行う。

<!-- 得られた結果を書く -->

## 背景

pandasの`read_sql`メソッドは`chunksize`を渡すことで一度に読み込むタプルの個数を制限できるが、素朴な使い方ではクライアント側で全てを読み込んでしまう。これを回避するためにはSQLAlchemyでサーバーサイドカーソルを使うように設定をしなければならない[^1]。しかしながら、MySQLにおいてはサーバーサイドカーソルが使えないという情報がpandasのIssueに記載されている[^2]。
そこで、実際にそうなのかを確かめるために実験を行う。

## 方法

### 実験

RDBMSから`pandas.read_sql`を使ってデータベースから全てのタプルを取得するPythonのコードを書き、そのPythonのコードが使うメモリの量をmemory-profilerパッケージで計測する。

次の仮説を検証したい。

1. `pandas.read_sql`に`chunk_size`引数を渡すことでメモリ使用量が減少すること。
2. `chunk_size`を指定した時にstreamingを有効にすることでメモリ使用量が減少すること。
    1. MySQLでstreamingを有効にしたときにメモリ使用量が減少すること。
    2. PostgreSQLでstreamingを有効にした時にメモリ使用量が減少すること。

以下の設定での実験がMySQLとPostgreSQLに対して必要になる。

1. `chunk_size`の指定を_せず_、streamingの有効化も_しない_場合。
2. `chunk_size`の指定をして、streamingの有効化を_しない_場合。
3. `chunk_size`の指定を_せず_、streamingの有効化をする場合。
4. `chunk_size`の指定をして、streamingの有効化をする場合。

### 手順

実験の手順は以下の通りである。

1. RDBMSにN個のタプルを書き込む。
2. 検証したい仮説を実装したPythonプログラムを実行する。

RDBMSとPythonプログラムはそれぞれ別のDockerコンテナで実行する。ネットワーク等の設定はdocker composeを用いる。

手順1で使うプログラムを関数として実装する。これは手順2と同じPythonプログラムの中で実装される。

手順2で使うプログラムは仮説を関数として実装する。このとき、それぞれの関数にはデコレータ`@profile`をつけておくことで行ごとのメモリプロファイルを取得できるようにしておく。各々の関数はinvokeパッケージで起動できるようにしておく。

## 参考文献

[^1]: [Loading SQL data into Pandas without running out of memory](https://pythonspeed.com/articles/pandas-sql-chunking/)

[^2]: [Reading table with chunksize still pumps the memory #12265](https://github.com/pandas-dev/pandas/issues/12265)
