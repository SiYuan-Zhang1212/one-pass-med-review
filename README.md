# One Pass Med Review

一个本地优先的医学刷题复习助手。目标很直接：**每道题只做一遍，把做题过程沉淀成可复习资产，尽量避免反复回看题库浪费时间。**

One Pass Med Review is a local-first study assistant for medical question practice. The goal is simple: do each question once, capture the learning value, and avoid wasting review time by repeatedly browsing the same question bank.

## 中文说明

这个项目面向一种 Mac + iPhone 的复习工作流：

1. 在 Mac 上投屏 iPhone。
2. 在 iPhone 上正常使用医考帮等医学题库 App 做题。
3. 本地工具观察投屏窗口的题目区域。
4. OCR 提取题干、选项、答案和解析。
5. 程序记录做对/做错，并生成复习报告。

项目的核心理念不是“保存所有截图”或“复制题库”，而是把刷题过程转成结构化复习材料：

- 错题：记录错因、正确思路、易混点和复习提醒。
- 对题：只保留一句话知识点总结，避免过度复习。
- 截图：只在必要时保存证据，不长期保存连续录屏。

## 当前状态

这个仓库目前处于 MVP 骨架阶段。

已经完成：

- 用 SQLite 保存做题 session、题目记录和可选证据截图。
- 提供 CLI 命令，用于初始化数据库、创建 session、添加题目、生成 Markdown 报告。
- 定义了隐私和存储策略，避免把每秒截图长期保存到硬盘。
- 提供 repo 内置的 Codex skill 草稿，后续可用于 AI 辅助整理复习报告。
- 配置了基础测试和 GitHub Actions CI。

计划下一步：

- 选择 Mac 上的 iPhone 投屏窗口或指定区域。
- 接入 OCR，优先考虑中文识别质量。
- 添加快捷键标记“做对”“做错”“本题结束”。
- 加入可选 AI 总结，并保持本地优先和可审计。
- 导出 CSV、Anki 或更适合复习的 Markdown 报告。

## 设计原则

- 默认本地优先。
- 不保存连续录屏。
- 每秒截图只是临时输入，不是长期资料。
- 只在有价值时保存截图，尤其是错题证据。
- 做对题总结要短，做错题分析要清楚。
- 每一步自动化都要能被检查和纠正。

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

onepass init
onepass demo
```

创建一个真实 session：

```bash
onepass new-session --title "医考帮第一轮 - 呼吸系统" --source "iPhone mirrored to Mac"
```

在截屏和 OCR 层还没完成前，可以先手动添加题目测试报告流程：

```bash
onepass add-question \
  --session-id 1 \
  --outcome wrong \
  --stem "患者咳嗽、咳痰伴发热，胸片提示..." \
  --options-json '["肺炎链球菌肺炎", "肺结核", "支气管哮喘"]' \
  --selected-answer "肺结核" \
  --correct-answer "肺炎链球菌肺炎" \
  --explanation "典型表现和影像更符合肺炎链球菌肺炎。" \
  --summary "错因：把急性感染性表现误判为慢性病程。复习：肺炎链球菌肺炎常见铁锈色痰和大叶实变。"
```

生成 Markdown 报告：

```bash
onepass report --session-id 1 --output reports/session-1.md
```

## 项目结构

```text
.
├── docs/                         # 架构、路线图、隐私和存储策略
├── skills/one-pass-med-review/   # repo 内置 Codex skill 草稿
├── src/one_pass_med_review/      # Python 包
├── tests/                        # Pytest 测试
├── pyproject.toml
└── README.md
```

## 隐私和存储

推荐的生产流程是：

1. 只截取 iPhone 投屏区域。
2. 判断画面是否发生有意义变化。
3. 对变化帧运行 OCR。
4. 除非用户按快捷键或规则要求保留，否则立即丢弃原始截图。
5. 长期保存文本、结构化元数据、简短总结和少量证据截图。

完整策略见 [docs/privacy-and-storage.md](docs/privacy-and-storage.md)。

## 法律和平台边界

这个项目用于个人复习工作流，不应用来批量复制、分发或再发布受版权保护的题库内容。长期保存的理想材料应该是个人知识总结，而不是题库原文镜像。

## GitHub

仓库地址：[SiYuan-Zhang1212/one-pass-med-review](https://github.com/SiYuan-Zhang1212/one-pass-med-review)

## License

MIT. See [LICENSE](LICENSE).

---

## English

This project is designed for a Mac workflow where an iPhone screen is mirrored to the desktop, a local tool observes the mirrored question area, OCR extracts the visible content, and the app turns correct and wrong attempts into concise review assets.

## Status

This repository is at MVP scaffold stage.

Implemented now:

- SQLite storage for practice sessions, question records, and optional evidence screenshots.
- CLI commands to initialize storage, create sessions, add question records, and generate Markdown reports.
- A storage policy that avoids retaining continuous screenshots.
- A repo-contained Codex skill draft for future AI-assisted report processing.
- Basic tests and GitHub Actions CI.

Planned next:

- Window/region selection for the mirrored iPhone screen.
- OCR provider integrations.
- Hotkeys for "correct", "wrong", and "question finished".
- Optional AI summarization with local-first redaction controls.
- Anki and CSV export.

## Design Principles

- Local-first by default.
- Do not store a continuous recording.
- OCR frames are temporary inputs, not permanent data.
- Save screenshots only when they are useful evidence, especially for wrong questions.
- Keep summaries short for correct questions and more diagnostic for wrong questions.
- Make every automation step auditable before trusting it.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

onepass init
onepass demo
```

Create a real session:

```bash
onepass new-session --title "医考帮第一轮 - 呼吸系统" --source "iPhone mirrored to Mac"
```

Add a question manually while the capture/OCR layer is still being built:

```bash
onepass add-question \
  --session-id 1 \
  --outcome wrong \
  --stem "患者咳嗽、咳痰伴发热，胸片提示..." \
  --options-json '["肺炎链球菌肺炎", "肺结核", "支气管哮喘"]' \
  --selected-answer "肺结核" \
  --correct-answer "肺炎链球菌肺炎" \
  --explanation "典型表现和影像更符合肺炎链球菌肺炎。" \
  --summary "错因：把急性感染性表现误判为慢性病程。复习：肺炎链球菌肺炎常见铁锈色痰和大叶实变。"
```

Generate a Markdown report:

```bash
onepass report --session-id 1 --output reports/session-1.md
```

## Repository Layout

```text
.
├── docs/                         # Architecture and product notes
├── skills/one-pass-med-review/   # Repo-contained Codex skill draft
├── src/one_pass_med_review/      # Python package
├── tests/                        # Pytest suite
├── pyproject.toml
└── README.md
```

## Privacy and Storage

The intended production loop is:

1. Capture the mirrored iPhone region.
2. Detect whether the frame meaningfully changed.
3. Run OCR.
4. Discard the raw frame unless a rule or hotkey marks it as evidence.
5. Store text, structured metadata, short summaries, and selected evidence only.

See [docs/privacy-and-storage.md](docs/privacy-and-storage.md) for the full policy.

## Legal and Platform Boundaries

This project is intended for personal study workflows. It should not be used to bulk copy, redistribute, or republish proprietary question bank content. The safest long-term artifact is a personal knowledge summary, not a mirrored copy of the source material.
