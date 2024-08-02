# データベースに追加の情報を保存する方法

> [!Important]
>
> 同時に二人以上の開発者がデータベースのモデルを修正するタスクを取らないでください。他の方のデータベース修正タスクが終わってから次のタスクを取るようにしてください。
> Flask-Migrate を用いて管理しており、マイグレーションファイルは自動生成されるため、複数人でマイグレーションファイルを自動生成してしまうと解消が難しいコンフリクトに遭遇する可能性が高いです。

## 例: 例えばユーザーのフルネームを保存したくなったとき

1. ユーザー情報は `src/web/auth/models.py` の `User` にあるので、個々に追加したいプロパティを追記してください。
    ```diff
     class User(DB.Model, UserMixin):
         id = DB.Column(DB.Integer, primary_key=True)
         username = DB.Column(DB.String(128))
         hashed_password = DB.Column(DB.String(256))
    +    full_name = DB.Column(DB.String(256))
    ```
1. 追加した人がやること: `rye run flask db migrate` を実行する
    - `migrations` フォルダ以下にマイグレーションファイルが追加されるため、これをコミットしてください。
1. 全員がやること: `rye run flask db upgrade` を実行する
    - 追加した人も、追加されたマイグレーションファイルを `git pull` した人も、実際にデータベースに反映するためにこのコマンドを実行する必要があります。

## 例: もっと違う概念、たとえばアイテムを保存したくなったとき

1. 新しいモデル、例えば `Item` モデルを追加する場合は `src/web/models.py` に追記します。
    ```python
    class Item(DB.Model):
        id = DB.Column(DB.Integer, primary_key=True)
        user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'))
        name = DB.Column(DB.String(256))
        amount = DB.Column(DB.Integer)
    ```
1. 追加した人がやること: `rye run flask db migrate -m "説明を入力"` を実行する
    - `migrations` フォルダ以下にマイグレーションファイルが追加されるため、これをコミットしてください。
1. 全員がやること: `rye run flask db upgrade` を実行する
    - 追加した人も、追加されたマイグレーションファイルを `git pull` した人も、実際にデータベースに反映するためにこのコマンドを実行する必要があります。
