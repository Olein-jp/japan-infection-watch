"""照合済み JIHS 週次定点 CSV の収録範囲とハッシュを検証する。"""

import argparse
from datetime import date
import json
from pathlib import Path
import re

from apps.web.preview_data import history_start
from scripts.check_preview import SHA256


DEFAULT_INPUTS = Path(__file__).resolve().parents[1] / "config/jihs-reviewed-inputs.json"


def week_end(week):
    if not re.fullmatch(r"[0-9]{4}-W[0-9]{2}", week):
        raise ValueError(f"対象週の形式が不正です: {week}")
    return date.fromisocalendar(int(week[:4]), int(week[-2:]), 7)


def load_reviewed_inputs(path=DEFAULT_INPUTS):
    # JSON キーの重複を検知して、どのハッシュを使うかが曖昧な入力を拒否する。
    def unique(pairs):
        result = dict(pairs)
        if len(result) != len(pairs):
            raise ValueError("対象週が重複しています")
        return result

    raw = json.loads(path.read_bytes(), object_pairs_hook=unique)
    if not isinstance(raw, dict) or not raw:
        raise ValueError("対象週と SHA-256 を1件以上指定してください")
    if any(not isinstance(digest, str) or not SHA256.fullmatch(digest) for digest in raw.values()):
        raise ValueError("原本の SHA-256 を64桁の小文字の16進数で指定してください")
    if len(set(raw.values())) != len(raw):
        raise ValueError("複数週に同じ原本の SHA-256 を指定できません")
    ends = [week_end(week) for week in raw]
    if min(ends) < history_start(max(ends)):
        raise ValueError("直近6か月より前の対象週が含まれています")
    return dict(sorted(raw.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reviewed-inputs", type=Path, default=DEFAULT_INPUTS)
    args = parser.parse_args()
    try:
        print(json.dumps(load_reviewed_inputs(args.reviewed_inputs)))
    except (OSError, ValueError) as error:
        parser.exit(2, f"収録対象を確認できません：{error}\n")


if __name__ == "__main__":
    main()
