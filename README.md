# `pandas.DataFrame.read_sql`が使用するメモリサイズを測定する

このリポジトリにはPythonのライブラリであるpandasの`DataFrame.read_sql`メソッドが使用するメモリのサイズをいくつかの条件で測定するプログラムがある。
測定に使うRDBMSはMySQLとPostgreSQLの2つ、SQLAlchemyの`stream_results`フラグの値が`True`と`False`の2つの場合、`read_sql`の`chunksize`引数を渡す場合と渡さない場合の2つにについて測定を行う。
<!-- 得られた結果を書く -->

## 背景

pandasの`read_sql`メソッドは`chunksize`を渡すことで一度に読み込むタプルの個数を制限できるが、素朴な使い方ではクライアント側で全てを読み込んでしまう。これを回避するためにはSQLAlchemyでサーバーサイドカーソルを使うように設定をしなければならない[^1]。しかしながら、MySQLにおいてはサーバーサイドカーソルが使えないという情報がpandasのIssueに記載されている[^2]。
そこで、実際にそうなのかを確かめるために実験を行う。

## 方法

## 参考文献

[^1]: [Loading SQL data into Pandas without running out of memory](https://pythonspeed.com/articles/pandas-sql-chunking/)
[^2]: [Reading table with chunksize still pumps the memory #12265](https://github.com/pandas-dev/pandas/issues/12265)
