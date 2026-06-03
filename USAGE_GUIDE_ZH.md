# autonovel 使用说明（中文）

本指南回答两个核心场景：

1. 如何导出当前已经写好的书（原书）
2. 如何从头生成一本新书

适用目录：项目根目录。

---

## 0. 环境准备

```bash
# 进入项目
cd D:/dev/myAotoNovel/autonovel

# 安装依赖
uv sync

# 配置环境变量
copy .env.example .env
# 在 .env 中填写 DEEPSEEK_API_KEY
```

说明：
- 只跑核心写作流程时，至少需要 `DEEPSEEK_API_KEY`。
- 生成封面/插图需要 `FAL_KEY`。
- 生成有声书需要 `ELEVENLABS_API_KEY`。

---

## 1. 场景 A：导出原来的书（已有章节）

这个场景适合你已经有完整章节文件（`chapters/ch_*.md`），想重新导出成 manuscript 和 PDF。

### 1.1 一键导出（推荐）

```bash
uv run python run_pipeline.py --phase export
```

该命令会执行：
- 重建大纲（`build_outline.py`）
- 重建章节弧线摘要（`build_arc_summary.py`）
- 生成 `manuscript.md`
- 生成 LaTeX 中间文件（`typeset/chapters_content.tex`）
- 若系统有 `tectonic`，继续生成 `typeset/novel.pdf`

### 1.2 手动导出（分步排查时使用）

```bash
uv run python build_outline.py
uv run python build_arc_summary.py
uv run python typeset/build_tex.py
cd typeset
tectonic novel.tex
```

如果没有安装 `tectonic`：
- 仍可先得到 `typeset/chapters_content.tex`
- 后续可在有 TeX 环境的机器上编译

### 1.3 导出前检查清单

- `chapters/ch_*.md` 文件存在且非空
- `typeset/novel.tex` 存在
- `state.json` 不影响导出本身，但建议保留
- 若要导出旧版本，先切到对应分支

示例：
```bash
git checkout autonovel/bells
uv run python run_pipeline.py --phase export
```

---

## 2. 场景 B：生成一本新书（从 seed 到导出）

推荐流程是“新分支 + from-scratch”。

### 2.1 新建分支（避免污染旧书）

```bash
git checkout -b autonovel/my-new-book
```

### 2.2 生成或编写 seed

```bash
uv run python seed.py --count=1
```

把你要用的设定写入 `seed.txt`。

### 2.3 运行完整流水线

```bash
uv run python run_pipeline.py --from-scratch
```

默认顺序：
1. foundation（世界观/角色/大纲/canon/voice）
2. drafting（逐章生成）
3. revision（自动修订）
4. export（导出）

### 2.4 分阶段运行（推荐给长任务）

```bash
# 先打地基
uv run python run_pipeline.py --phase foundation --from-scratch

# 再写章节
uv run python run_pipeline.py --phase drafting

# 再修订
uv run python run_pipeline.py --phase revision --max-cycles 5

# 最后导出
uv run python run_pipeline.py --phase export
```

---

## 3. 推荐的“旧书导出 + 新书生成”顺序

如果你同时要做这两件事，建议按下面顺序：

1. 切到旧书分支，先导出原书
2. 回到主干或模板分支
3. 新建新书分支
4. 生成新书 foundation
5. 继续 drafting/revision/export

示例：

```bash
# A. 导出旧书
git checkout autonovel/bells
uv run python run_pipeline.py --phase export

# B. 生成新书
git checkout master
git checkout -b autonovel/new-project-2026
uv run python seed.py --count=1
# 手动编辑 seed.txt
uv run python run_pipeline.py --phase foundation --from-scratch
uv run python run_pipeline.py --phase drafting
uv run python run_pipeline.py --phase revision --max-cycles 5
uv run python run_pipeline.py --phase export
```

### 3.1 可选：一键归档并重置（不切分支也可用）

如果你希望“导出后自动保存当前书，再清空工作区准备新书”，可以用：

```bash
uv run python archive_and_reset.py --yes
```

脚本行为：
- 把当前书相关产物归档到 `archives/时间戳_书名/`
- 清空 `chapters/`、`briefs/`、`edit_logs/`、`eval_logs/`
- 重置 `seed.txt`、`world.md`、`characters.md`、`outline.md`、`canon.md`、`MYSTERY.md`、`state.json`
- 保留 `voice.md` 的 Part 1，并把 Part 2 置为待生成

常用参数：

```bash
# 只归档，不重置
uv run python archive_and_reset.py --archive-only --yes

# 指定归档标签（目录名更清晰）
uv run python archive_and_reset.py --tag bells-final --yes
```

建议：
- 即使使用这个脚本，仍建议“一书一分支”，便于历史追溯和回滚。
- 第一次使用时先运行 `--archive-only` 确认归档内容符合预期。

---

## 4. 常见问题

### Q1: foundation 通过了，但流程停在 drafting 之前？
正常。`foundation` 跑完后会把 `state.json` 更新到 drafting。你可以直接执行：

```bash
uv run python run_pipeline.py --phase drafting
```

### Q2: 为什么只跑了 foundation，没有继续跑完整本书？
因为你指定了 `--phase foundation`。若要全流程请用：

```bash
uv run python run_pipeline.py --from-scratch
```

### Q3: 只想验证评估器和风格指纹是否正常？

```bash
uv run python evaluate.py --phase=foundation
uv run python voice_fingerprint.py
```

---

## 5. 最小命令速查

```bash
# 导出旧书
uv run python run_pipeline.py --phase export

# 新书从头跑全流程
uv run python run_pipeline.py --from-scratch

# 只跑 foundation
uv run python run_pipeline.py --phase foundation --from-scratch
```
