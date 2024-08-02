#!/bin/bash

set -eo pipefail

# Rye を有効化する
source ~/.rye/env

# Rye で依存関係をインストールする
rye sync

# (可能なら) マイグレーションを実行する
rye run flask db init || true
rye run flask db upgrade || true

~/.cargo/bin/watchexec --poll 100 -r --exts py,html -v -- \
  rye run flask --debug run --no-reload --host 0.0.0.0
