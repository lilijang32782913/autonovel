@echo off
setlocal

REM ======================================================
REM 按你的项目需求修改以下约束
REM ======================================================

set BRIEF_FILE=seed_brief_template.md
set COUNT=3

set PROJECT=写一部情感张力强、世界观不套路化的奇幻小说。
set RIFF=

set MUST_HAVE_1=魔法必须有真实且不可逆的代价。
set MUST_HAVE_2=个人冲突与世界级冲突必须正面碰撞。
set MUST_HAVE_3=至少包含一个能推动剧情的非常规环境要素。

set MUST_AVOID_1=天选之子预言。
set MUST_AVOID_2=魔法学院设定。
set MUST_AVOID_3=黑暗魔王作为核心反派。

set TONE_1=忧郁但仍有希望。
set TONE_2=文学感与清晰剧情推进并存。

set SETTING_1=避开标准中世纪欧洲编码。
set SETTING_2=地理与物质文化要有高感官具体性。

set PROTAGONIST_1=主角有与魔法代价绑定的私人愧疚。
set PROTAGONIST_2=主角能力越强，越会制造新问题。

set MAGIC_COST_1=每次施法都要牺牲一段有意义的记忆。
set MAGIC_COST_2=不能存在可完全规避代价的漏洞。

REM ======================================================
REM 执行命令
REM ======================================================

if "%RIFF%"=="" (
  uv run python seed.py ^
    --count %COUNT% ^
    --project "%PROJECT%" ^
    --brief-file "%BRIEF_FILE%" ^
    --must-have "%MUST_HAVE_1%" ^
    --must-have "%MUST_HAVE_2%" ^
    --must-have "%MUST_HAVE_3%" ^
    --must-avoid "%MUST_AVOID_1%" ^
    --must-avoid "%MUST_AVOID_2%" ^
    --must-avoid "%MUST_AVOID_3%" ^
    --tone "%TONE_1%" ^
    --tone "%TONE_2%" ^
    --setting "%SETTING_1%" ^
    --setting "%SETTING_2%" ^
    --protagonist "%PROTAGONIST_1%" ^
    --protagonist "%PROTAGONIST_2%" ^
    --magic-cost "%MAGIC_COST_1%" ^
    --magic-cost "%MAGIC_COST_2%" ^
    --save-output
) else (
  uv run python seed.py ^
    --riff "%RIFF%" ^
    --project "%PROJECT%" ^
    --brief-file "%BRIEF_FILE%" ^
    --must-have "%MUST_HAVE_1%" ^
    --must-have "%MUST_HAVE_2%" ^
    --must-have "%MUST_HAVE_3%" ^
    --must-avoid "%MUST_AVOID_1%" ^
    --must-avoid "%MUST_AVOID_2%" ^
    --must-avoid "%MUST_AVOID_3%" ^
    --tone "%TONE_1%" ^
    --tone "%TONE_2%" ^
    --setting "%SETTING_1%" ^
    --setting "%SETTING_2%" ^
    --protagonist "%PROTAGONIST_1%" ^
    --protagonist "%PROTAGONIST_2%" ^
    --magic-cost "%MAGIC_COST_1%" ^
    --magic-cost "%MAGIC_COST_2%" ^
    --save-output
)

endlocal
