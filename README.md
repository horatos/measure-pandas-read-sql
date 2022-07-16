# `pandas.DataFrame.read_sql`が使用するメモリサイズを測定する

このリポジトリには、Pythonのライブラリであるpandasの`DataFrame.read_sql`メソッドが使用するメモリのサイズを、いくつかの条件で測定するプログラムがある。
このプログラムを書いた理由は、pandasはMySQLを利用する場合にサーバーサイドカーソルを有効にできずメモリ使用量を削減できないという情報があり、このことを検証したいからである。

測定に使うRDBMSはMySQL 8とMySQL 5.7とPostgreSQLの3つである。
SQLAlchemyの`execution_options`に`stream_results=True`を渡す場合と`execution_options`を呼ばない場合、`read_sql`の`chunksize`引数を渡す場合と渡さない場合を組み合わせた全部で4通りの条件で測定を行う。

実験の結果ではどのRDBMSでも`execution_options(stream_results=True)`を呼び、`DataFrame.read_sql`に`chunksize`を渡した場合には、消費メモリ量が減少した。したがって、`pandas`でサーバーサイドカーソルが利用できると思われる。

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

これらの手順を *./app* 以下のPythonプログラムに実装した。また、*run.sh* を実行することですべての実験が実行される。

実験に用いたライブラリのバージョンは以下のとおりである。

| ライブラリ      | バージョン|
|:----------------|:----------|
| pandas          | 1.4.3     |
| sqlalchemy      | 1.4.39    |
| PyMySQL         | 1.0.2     |
| psycopg2-binary | 2.9.3     |

## 結果

データベースに格納する行数を10万行、chunksizeを1000としたときの実験結果を docs/results-1.txt に保存してある。

実験1のメモリ使用量は`pd.read_sql`のIncrementを採用する。
というのも、この操作ですべての行を読み込むからである。
実験記録から使用量はMySQL 8が45.9 MiB、MySQL 5.7が46.0 MiB、PostgreSQLが70.9 MiBである。

実験2のメモリ使用量は`pd.read_sql`と`for chunk in it`のIncrementの合計を採用する。
というのも、この2つの操作で行を読み込んでいくからである。
実験記録から使用量はMySQL 8が40.6 MiB、MySQL 5.7が40.6 MiB、PostgreSQLが30.7 MiBである。

実験3のメモリ使用量は、実験1と同様に、`pd.read_sql`のIncrementを採用する。
実験記録から使用量はMySQL 8が44.1 MiB、MySQL 5.7が43.3 MiB、PostgreSQLが71.4 MiBである。

実験4のメモリ使用量は、実験2と同様に、`pd.read_sql`と`for chunk in it`のIncrementの合計を採用する。
実験記録から使用量はMySQL 8が2.5 MiB、MySQL 5.7が2.4 MiB、PostgreSQLが3.6 MiBである。

|        | MySQL 8  | MySQL 5.7 | PostgreSQL |
|:------:|---------:|----------:|-----------:|
| 実験1  | 45.9 MiB |  46.0 MiB |   70.9 MiB |
| 実験2  | 40.6 MiB |  40.6 MiB |   30.7 MiB |
| 実験3  | 44.1 MiB |  43.3 MiB |   71.4 MiB |
| 実験4  |  2.5 MiB |   2.4 MiB |    3.6 MiB |

## 議論

予想に反してMySQLでもPostgreSQLでも共にサーバーサイドカーソルが利用できることがわかった。
pandas-dev/pandas#12265 の報告は2016年になされたものなので、2022年現在はPyMySQLでもサーバーサイドカーソルが利用できるようになったと考えるのがよいだろう。

いずれの場合でもサーバーサイドカーソルを有効にした上でchunksizeを指定して読み込むことで、消費するメモリの量を大きく減らせることがわかった。

すべての行を一度に読み込む動作になっている実験1と実験3においてPostgreSQLを利用した場合に消費するメモリが約70 MiBと、MySQLのそれに比べ2倍近くになっている。詳細を調べていないのでこの原因はわからない。

## 結論

`pandas`で`DataFrame.read_sql`を呼ぶ際に、適切な設定を行えばサーバーサイドカーソルの利用が可能になりメモリ使用量が抑えられる。
Issue pandas-dev/pandas#12265 は古い情報であり、SQLドライバのアップデートによりMySQLでもサーバーサイドカーソルが利用できるようになったと思われる。

[^1]: [Loading SQL data into Pandas without running out of memory](https://pythonspeed.com/articles/pandas-sql-chunking/)

[^2]: [Reading table with chunksize still pumps the memory #12265](https://github.com/pandas-dev/pandas/issues/12265)
