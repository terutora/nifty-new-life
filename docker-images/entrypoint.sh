#!/bin/bash

set -eo pipefail

# Rye を有効化する
source ~/.rye/env

# データベースの起動を待つ
# Fargateでタスク起動時のdepends_onのcondition=STARTでは不十分なため、sleepで待つ
sleep 60

# マイグレーションを実行する
rye run flask --app /app/src/web/app.py db init || true
rye run flask --app /app/src/web/app.py db upgrade || true

rye run waitress-serve --call 'web.app:create_app'
