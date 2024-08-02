import os

from werkzeug.routing import Rule


# これは以下のようなベースパスの切り替えを実現するためのカスタムルールです。
# - ローカル: /foo/bar/...
# - AWS 上: /{team_name}/foo/bar/...
# 新しいパスを追加するためにこのクラスを修正する必要はありません。
class AddTeamNamePrefixCustomRule(Rule):
    def __init__(self, string, *args, **kwargs):
        team_name = os.getenv("TEAM_NAME", "").strip("/")
        base_path = f"/{team_name}".rstrip("/")
        super().__init__(f"{base_path}/{string}", *args, **kwargs)
