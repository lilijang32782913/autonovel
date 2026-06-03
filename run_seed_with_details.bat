@echo off
setlocal

REM ======================================================
REM Edit these lines for your own project constraints
REM ======================================================

set BRIEF_FILE=seed_brief_template.md
set COUNT=3

set PROJECT=Write a fantasy novel with strong emotional stakes and a non-generic world.
set RIFF=

set MUST_HAVE_1=Magic has a real irreversible cost.
set MUST_HAVE_2=Personal conflict and cosmic conflict must directly collide.
set MUST_HAVE_3=At least one unusual environmental feature that drives plot.

set MUST_AVOID_1=Chosen one prophecy.
set MUST_AVOID_2=Magic school setting.
set MUST_AVOID_3=Dark lord as central antagonist.

set TONE_1=Melancholy but hopeful.
set TONE_2=Literary with clear plot momentum.

set SETTING_1=Outside standard medieval Europe coding.
set SETTING_2=High sensory specificity in geography and material culture.

set PROTAGONIST_1=Protagonist has a private guilt tied to the magic cost.
set PROTAGONIST_2=Protagonist competence should create new problems.

set MAGIC_COST_1=Each use of magic sacrifices a meaningful memory.
set MAGIC_COST_2=No loophole that nullifies the cost.

REM ======================================================
REM Command
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
