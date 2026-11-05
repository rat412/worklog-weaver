#!/usr/bin/env python3
"""collect_gitlog.py — 从 git 历史生成周报原料草稿（仅 Python 标准库）。

用法:
    python collect_gitlog.py --since 7d --repo /path/to/repo --out raw_material.md
    python collect_gitlog.py --since 2026-10-01 --repo repoA --repo repoB --author alice

--since 支持:
    Nd   最近 N 天（如 7d）
    Nw   最近 N 周（如 2w）
    YYYY-MM-DD  自该日期起
"""
import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta


def parse_since(value):
    m = re.fullmatch(r"(\d+)d", value)
    if m:
        return (datetime.now() - timedelta(days=int(m.group(1)))).strftime("%Y-%m-%d")
    m = re.fullmatch(r"(\d+)w", value)
    if m:
        return (datetime.now() - timedelta(weeks=int(m.group(1)))).strftime("%Y-%m-%d")
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        raise SystemExit(f"无法解析 --since: {value}（支持 7d / 2w / YYYY-MM-DD）")


def collect(repo, since, author=None):
    fmt = "%ad%x09%s"  # date<TAB>subject
    cmd = ["git", "-C", repo, "log", f"--since={since}",
           f"--pretty=format:{fmt}", "--date=short", "--no-merges"]
    if author:
        cmd.append(f"--author={author}")
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[警告] {repo} 读取失败: {e.stderr.strip()}", file=sys.stderr)
        return []
    except FileNotFoundError:
        raise SystemExit("未找到 git 命令，请先安装 git。")
    lines = [l for l in out.stdout.splitlines() if "\t" in l]
    return [(repo, *l.split("\t", 1)) for l in lines]


def main():
    ap = argparse.ArgumentParser(description="git 历史 → 周报原料草稿")
    ap.add_argument("--repo", action="append", required=True,
                    help="仓库路径，可多次指定")
    ap.add_argument("--since", default="7d", help="起始时间，默认 7d")
    ap.add_argument("--author", default=None, help="按作者过滤（可选）")
    ap.add_argument("--out", default=None, help="输出文件，默认打印到 stdout")
    args = ap.parse_args()

    since = parse_since(args.since)
    entries = []
    for repo in args.repo:
        entries.extend(collect(repo, since, args.author))
    entries.sort(key=lambda e: e[1])  # 按日期排序

    lines = [
        f"# 原料清单（git 来源）",
        f"",
        f"- 时间范围: {since} 起",
        f"- 仓库: {', '.join(args.repo)}",
        f"- 提交条数: {len(entries)}",
        f"",
    ]
    for i, (repo, date, subject) in enumerate(entries, 1):
        lines.append(f"#{i}  [{date}] {subject} (git: {repo})")
    if not entries:
        lines.append("（该时间范围内无提交记录；请用笔记/待办/口述补充原料）")
    lines.append("")
    lines.append("> 提示：本清单只做归并去重，不做润色。"
                 "请补充笔记、待办与口述原料后，再进入分类归并步骤。")
    text = "\n".join(lines) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"已写入 {args.out}（{len(entries)} 条）")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
