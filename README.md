# worklog-weaver

**一句话定位**：把零散的工作痕迹（git 提交、笔记、待办）编织成事实先行、拒绝套话的结构化周报 / 月报 / 述职素材。

**One-liner (EN)**: Weave scattered work traces (git commits, notes, todos) into structured, fact-first weekly / monthly / review reports — no filler phrases, every claim traceable.

---

## 效果与流程 / How it works

```
git log / 笔记 / 待办 / 口述
        │
        ▼
  ① 原料清单（一行一条，可溯源）
        │
        ▼
  ② 分类归并（3–5 个主题板块）
        │
        ▼
  ③ 套用模板（周报 / 月报 / 述职）
        │
        ▼
  ④ 量化改写（对照词库）
        │
        ▼
  ⑤ 反套话自检 → 成稿 + 原料映射
```

- **事实先行**：每条结论都能回溯到一条原始工作痕迹，不编造、不夸大。
- **拒绝套话**：内置反套话检查清单，"积极推进""持续优化"类表述会被标记并要求补事实。
- **一料多用**：同一份原料库，可分别产出周报、月报、述职素材。

## 目录结构 / Directory tree

```
worklog-weaver/
├── SKILL.md                          # 技能定义（frontmatter + 工作流程）
├── README.md                         # 本文件
├── references/
│   ├── structure-guide.md            # 三段式结构 + 分类维度 + 场景差异
│   └── quantification-phrases.md     # 量化表述词库（模糊 → 量化对照）
├── checklists/
│   └── pre-submit-check.md           # 提交前反套话自检清单
├── templates/
│   ├── weekly.md.tmpl                # 周报模板
│   ├── monthly.md.tmpl               # 月报模板
│   └── review.md.tmpl                # 述职/绩效素材模板
├── examples/
│   └── example-weekly.md             # 完整周报示例（含原料映射）
└── scripts/
    └── collect_gitlog.py             # git 历史 → 原料草稿（仅标准库）
```

## 使用方式 / Usage

**作为 Agent Skill**：将本目录放入你的技能目录（如 `~/.agent/skills/`），对 Agent 说：

> 帮我写本周周报 / write my weekly report / 整理这周的工作

Agent 会自动加载本技能，按五步流程执行。

**手动使用脚本**（可选，仅 Python 标准库）：

```bash
python scripts/collect_gitlog.py --since 7d --repo /path/to/repo --out raw_material.md
# 支持多个仓库
python scripts/collect_gitlog.py --since 2026-10-01 --repo repoA --repo repoB --author alice
```

**手动套模板**：复制 `templates/` 下对应模板，按 `references/structure-guide.md` 填充即可。

## 关键词 / Keywords

周报, 月报, 述职, 工作总结, 工作汇报, weekly report, monthly report, work summary, status update, performance review, git log, agent skill, AI agent, 结构化写作, 反套话, 量化表达

---

## English Introduction

worklog-weaver is an agent skill that turns scattered work traces — git commits, scratch notes, todo lists, chat highlights — into structured weekly reports, monthly reports, and performance-review material. It enforces a fact-first workflow: collect raw material → group into themes → apply a template → quantify vague statements → run an anti-cliché checklist before anything is submitted. Every claim in the final report maps back to a raw trace, so the output is auditable by construction.

The skill is mostly configuration and documentation: templates, reference guides, and one optional stdlib-only Python script that drafts raw material from git history.
