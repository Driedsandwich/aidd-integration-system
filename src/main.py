import argparse
import json
import os
import sys
import time
from typing import Dict, Iterable, List, Optional, Tuple

from urllib.parse import urlencode
from urllib.request import Request, urlopen


GITHUB_API_BASE = "https://api.github.com"


def build_headers(token: Optional[str]) -> Dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "cursor-aidd-sandbox-issues-cli",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def parse_link_header(link_header: Optional[str]) -> Dict[str, str]:
    links: Dict[str, str] = {}
    if not link_header:
        return links
    parts = [p.strip() for p in link_header.split(",")]
    for part in parts:
        if ";" not in part:
            continue
        url_part, rel_part = part.split(";", 1)
        url = url_part.strip().lstrip("<").rstrip(">")
        if "rel=" in rel_part:
            rel = rel_part.split("rel=")[-1].strip().strip('"')
            links[rel] = url
    return links


def fetch_issues(owner: str,
                 repo: str,
                 token: Optional[str],
                 state: str = "open",
                 per_page: int = 100) -> Iterable[Dict]:
    if per_page < 1 or per_page > 100:
        raise ValueError("per_page は 1..100 の範囲で指定してください")

    params = {"state": state, "per_page": str(per_page)}
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues?{urlencode(params)}"
    headers = build_headers(token)

    while url:
        req = Request(url, headers=headers, method="GET")
        try:
            with urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for item in data:
                    yield item
                link_header = resp.headers.get("Link")
                links = parse_link_header(link_header)
                url = links.get("next")
        except Exception as e:
            raise RuntimeError(f"GitHub API 呼び出しに失敗しました: {e}")


def filter_out_pull_requests(items: Iterable[Dict], include_prs: bool) -> Iterable[Dict]:
    for item in items:
        if include_prs:
            yield item
        else:
            if "pull_request" not in item:
                yield item


def to_table(rows: List[Tuple[str, str, str, str]]) -> str:
    # rows: [(number, state, title, html_url)]
    if not rows:
        return "(no issues)"

    headers = ("#", "state", "title", "url")
    cols = list(zip(*([headers] + rows)))  # transpose
    widths = [max(len(str(v)) for v in col) for col in cols]

    def fmt_line(values: Tuple[str, str, str, str]) -> str:
        return "  ".join(str(v).ljust(w) for v, w in zip(values, widths))

    lines = [fmt_line(headers), fmt_line(tuple("-" * w for w in widths))]
    for r in rows:
        lines.append(fmt_line(r))
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="GitHub の Issue 一覧を取得して表示します")
    parser.add_argument("repo", help="対象リポジトリ (例: owner/repo)")
    parser.add_argument("--state", choices=["open", "closed", "all"], default="open", help="Issueの状態")
    parser.add_argument("--format", choices=["json", "table"], default="json", help="出力形式")
    parser.add_argument("--include-prs", action="store_true", help="PRを含めて表示する（デフォルトは除外）")
    parser.add_argument("--per-page", type=int, default=100, help="1ページの件数 (1..100)")
    parser.add_argument("--token", default=os.getenv("GITHUB_TOKEN"), help="GitHubトークン（未指定時は環境変数 GITHUB_TOKEN を使用）")

    args = parser.parse_args(argv)

    if "/" not in args.repo:
        print("repo は owner/repo の形式で指定してください", file=sys.stderr)
        return 2

    owner, repo = args.repo.split("/", 1)

    try:
        items_iter = fetch_issues(owner=owner, repo=repo, token=args.token, state=args.state, per_page=args.per_page)
        items_iter = filter_out_pull_requests(items_iter, include_prs=args.include_prs)
        items = list(items_iter)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(items, ensure_ascii=False, indent=2))
    else:
        rows: List[Tuple[str, str, str, str]] = []
        for it in items:
            number = f"#{it.get('number')}"
            state = it.get("state", "")
            title = (it.get("title", "") or "").replace("\n", " ")
            url = it.get("html_url", "")
            rows.append((number, state, title, url))
        print(to_table(rows))

    return 0


if __name__ == "__main__":
    sys.exit(main())

