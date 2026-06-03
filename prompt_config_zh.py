"""全中文 LLM 提示词中心配置。"""

SEED_SYSTEM = (
    "你是一名奇幻小说策划编辑与小说家。"
    "你生成的创意必须具体、可落地、具有结构张力，避免套路化设定。"
    "禁止空泛形容与模板化口号。"
)

SEED_GENERATE_PROMPT = """请生成 {count} 个奇幻小说 seed 创意，每个都要可直接进入长篇创作。

每个创意都包含：

1. 标题（有辨识度，避免通用词拼贴）
2. 钩子（1 句话，让读者愿意翻开）
3. 世界设定（必须具体且有感官细节）
4. 魔法与代价（能力与限制并重，且代价能制造两难）
5. 冲突（个人冲突 + 世界级冲突，并且二者互相拉扯）
6. 主题问题（一个没有标准答案的问题）
7. 非套路说明（为什么不是常见奇幻套路）

要求：
- {count} 个创意在题材气质、叙事结构、冲突类型上要有明显差异
- 禁止：天选之子预言（除非有强反转）、纯“黑暗魔王”主反派、魔法学院模板、恋爱三角主驱动
"""

SEED_RIFF_PROMPT = """我有一个 seed 想法：

"{idea}"

请基于这个想法生成 5 个方向明显不同的变体。
每个变体都包含：
- 标题
- 钩子（1 句话）
- 差异说明（你改了什么，为什么这样改）
- 世界设定（具体且可感知）
- 魔法与代价
- 冲突（个人 + 世界）
- 主题问题

要求：不要只做表层改名换皮，必须改变至少两项：主角类型、结构、冲突核心、叙事气质。
"""

SEED_GUIDED_PROMPT = """请根据用户提供的详细约束，生成 {count} 个奇幻小说 seed 创意。

用户约束如下：
{guidance}

每个创意输出：
- 标题
- 钩子（1 句话）
- 世界设定
- 魔法与代价
- 冲突（个人 + 世界）
- 主题问题
- 非套路说明

硬规则：
- 严格满足 MUST-HAVE
- 严格避开 MUST-AVOID
- 若约束与常见写法冲突，优先约束
- 创意之间保持差异
"""

WORLD_SYSTEM = (
    "你是世界观总设计师。"
    "你输出的是可执行的世界圣经，而不是散文化简介。"
    "每条规则都要可检验，每条设定都要有社会后果。"
)

WORLD_PROMPT = """请编写本书的 WORLD.MD（世界圣经，中文）。

SEED：
{seed}

叙事声音：
{voice_part2}

写作约束：
{craft}

请按以下结构输出：
## 宇宙观与历史
## 魔法系统
### 硬规则
### 代价与限制
### 社会后果
## 地理与空间
## 势力与政治
## 文化日常
## 生态与自然异常
## 一致性约束（不可违背）

要求：
- 具体、可验证、可用于后续写作
- 每节都避免空话
- 中文输出
"""

CHARACTERS_SYSTEM = (
    "你是角色总设计师。"
    "你负责产出可直接驱动剧情的角色档案，强调因果链与区分度。"
)

CHARACTERS_PROMPT = """请编写本书的 CHARACTERS.MD（角色注册表，中文）。

SEED：
{seed}

WORLD：
{world}

叙事声音：
{voice_part2}

要求：
- 主要角色都要有：创伤/欲望/需求/谎言（因果链）
- 给出能区分说话方式的特征（词汇、句长、语气、回避习惯）
- 每个关键角色至少 1 个“若曝光会改变剧情”的秘密
- 角色之间的目标必须互相牵制，而非平行无交集

建议结构：
## 主角
## 核心对手
## 关键同盟
## 关键配角
## 关系图（文字版）
## 对话风格速查
"""

OUTLINE_SYSTEM = (
    "你是小说结构师。"
    "你输出可直接开写的章节大纲，重视节奏、伏笔与情绪推进。"
)

OUTLINE_PROMPT = """请生成完整长篇章节大纲（中文），目标 22-26 章。

SEED：
{seed}

中心谜题（作者视角）：
{mystery}

WORLD：
{world}

CHARACTERS：
{characters}

VOICE：
{voice_part2}

CRAFT：
{craft}

输出要求：
1. 先给三幕结构与关键百分比节点
2. 再给逐章大纲，章节标题格式统一为：### 第N章：标题
3. 每章包含：POV、地点、功能节拍、情绪弧线、关键事件、伏笔种下/回收、章末悬问、目标字数
4. 文末附“伏笔账本”表格

硬约束：
- 剧情可写、可拍、可评估，避免空泛摘要
- 伏笔种下与回收有明确章节编号
- 中文输出
"""

OUTLINE_CONT_SYSTEM = (
    "你是续写大纲的结构编辑。"
    "保持前文格式一致，补齐后半程并完善伏笔账本。"
)

OUTLINE_CONT_PROMPT = """下面是已有的大纲前半部分，请继续补齐后续章节并输出完整伏笔账本（中文）。

已有大纲：
{part1}

中心谜题：
{mystery}

要求：
- 延续既有章节格式（### 第N章：标题）
- 补齐到完整长篇（建议 24 章，允许 22-26）
- 补写并完善“伏笔账本”
- 确保主角弧线在结尾完成核心选择
"""

CANON_SYSTEM = (
    "你是连续性编辑。"
    "只提取硬事实，不脑补，不润色。"
)

CANON_PROMPT = """请从以下文档提取 CANON.MD（中文硬事实库）。

SEED：
{seed}

WORLD：
{world}

CHARACTERS：
{characters}

输出分类：
## 地理
## 时间线
## 魔法规则
## 角色硬事实
## 势力政治
## 文化习俗
## 已发生事件

规则：
- 一条一事实
- 必须可核验
- 标注来源（world.md / characters.md / seed.txt）
- 若冲突，显式标记“冲突待定”
"""

VOICE_SYSTEM = (
    "你是文学声音设计师。"
    "你提供的是可执行的写作声音规范，而不是赞美性描述。"
)

VOICE_PROMPT = """请为本书生成 voice.md 的 Part 2（中文）。

SEED：
{seed}

WORLD：
{world}

CHARACTERS：
{characters}

OUTLINE：
{outline}

输出结构：
## 声音总论
## 句法节奏
## 词汇与意象域
## 对话习惯
## 感官偏好
## 正例片段 1
## 正例片段 2
## 反例片段
## 校准清单（Do / Don't）

要求：
- 具体、可执行
- 与本书设定强绑定
- 约 900-1400 字
"""

DRAFT_SYSTEM = (
    "你是长篇小说中文写作模型。"
    "你必须按大纲完整写完一章，不可摘要，不可跳写。"
)

DRAFT_PROMPT = """请写第 {chapter_num} 章（中文完整正文）。

声音规范：
{voice}

本章大纲：
{chapter_outline}

下一章信息（用于衔接）：
{next_chapter}

上一章结尾：
{prev_tail}

世界观：
{world}

角色信息：
{characters}

一致性事实库：
{canon}

写作要求：
1. 严格覆盖本章关键节拍
2. 以场景为主，避免空泛总结
3. 对话有角色区分度
4. 细节具体，不使用模板化陈词
5. 章末形成自然推进
6. 输出完整章节正文
"""

REVISION_SYSTEM = (
    "你是小说修订编辑。"
    "你根据修订 brief 定向改稿，保留有效内容，修复问题点。"
)

REVISION_PROMPT = """请重写第 {ch_num} 章（中文），严格执行修订说明。

修订说明：
{brief}

声音规范：
{voice}

角色：
{characters}

世界观：
{world}

上一章结尾：
{prev_tail}

下一章开头：
{next_head}

当前草稿：
{old_text}

输出要求：
- 给出完整修订后章节正文
- 保持连续性
- 按 brief 优先级处理问题
"""

REVIEW_PROMPT = """请阅读以下小说《{title}》。
先以文学评论者视角给出整体评价，再以创意写作教师视角给出可执行改进建议。
可以指出优点，也可以指出问题；请公平、具体。

{manuscript}
"""

REVIEW_SYSTEM = (
    "你是资深文学评论与写作教学顾问。"
    "你的反馈需要兼顾审美判断与可执行改进建议，避免空泛夸赞。"
)

READER_SYSTEM_EDITOR = (
    "你是大型出版社的资深小说编辑。"
    "你关注叙事声音一致性、句法质感、潜台词与过度解释问题。"
    "反馈精确、具体，并仅输出合法 JSON。"
)

READER_SYSTEM_GENRE = (
    "你是高强度奇幻类型读者。"
    "你关注节奏、谜题推进、世界观兑现与阅读粘性。"
    "若剧情停滞或张力回落要直说，并仅输出合法 JSON。"
)

READER_SYSTEM_WRITER = (
    "你是已出版多部长篇的奇幻作家。"
    "你从技法层评估结构、伏笔回收、人物弧线与完成度。"
    "你重视目标与实现之间的差距，并仅输出合法 JSON。"
)

READER_SYSTEM_FIRST = (
    "你是认真但非专业的普通读者。"
    "你主要表达真实阅读感受：被打动、无聊、困惑、兴奋。"
    "少用术语，直接说体验，并仅输出合法 JSON。"
)

READER_PANEL_PROMPT = """你读完了一部长篇小说的结构化摘要。

{arc_summary}

请从“整本书”角度回答问题，并输出 JSON：
{{
  "momentum_loss": "在哪些章节掉速？为什么？",
  "earned_ending": "结尾是否由前文充分支撑？",
  "cut_candidate": "若必须压缩 10%，优先裁哪里？",
  "missing_scene": "缺少哪一场必须出现的戏？",
  "thinnest_character": "最薄弱角色是谁？",
  "best_scene": "最佳场景是哪一段？",
  "worst_scene": "最弱场景是哪一段？",
  "would_recommend": "是否推荐？推荐给谁？",
  "haunts_you": "最有余味的一句/一幕是什么？",
  "next_book": "你会读作者下一本吗？"
}}
"""

ADV_EDIT_SYSTEM = (
        "你是严厉但精确的文学编辑。"
        "你只基于原文给出可执行删改建议，不编造引文，并仅输出合法 JSON。"
)

ADV_EDIT_PROMPT = """你正在编辑一章奇幻小说，目标是找出该章最该删改的内容。\
请严格引用原文，并给出具体理由与动作。

章节全文（{word_count} 词）：
{chapter_text}

任务：
1. 找出 10-20 处应删减或重写的片段。
2. 每条必须包含：原文引用（至少 10 个词）、问题类型、原因、动作。
3. 类型仅可为：FAT / REDUNDANT / OVER-EXPLAIN / GENERIC / TELL / STRUCTURAL。
4. 若动作为 REWRITE，给出替换文本；若 CUT，rewrite 填 null。
5. 估算本章可安全删减的总词数。

输出 JSON：
{{
    "cuts": [
        {{
            "quote": "原文引用",
            "type": "FAT|REDUNDANT|OVER-EXPLAIN|GENERIC|TELL|STRUCTURAL",
            "reason": "问题说明",
            "action": "CUT or REWRITE",
            "rewrite": "替换文本或 null"
        }}
    ],
    "total_cuttable_words": N,
    "tightest_passage": "最不该动的 2-3 句",
    "loosest_passage": "最松散的 2-3 句",
    "overall_fat_percentage": N,
    "one_sentence_verdict": "一句话判断本章优势与拖累"
}}
"""

COMPARE_SYSTEM = (
        "你是小说编辑，负责在两章中强制选出更优者。"
        "不允许平票，必须给出决定性证据，并仅输出合法 JSON。"
)

COMPARE_PROMPT = """比较同一部小说的两章草稿，必须选出胜者（不能平局）。

章节 A（第 {ch_a} 章）：
{text_a}

章节 B（第 {ch_b} 章）：
{text_b}

比较维度：
- 语言是否更具体、更少泛化
- 对话是否像真实说话
- 张力/惊喜是否更有效
- 是否更信任读者（少解释）
- AI 写作痕迹是否更少

输出 JSON：
{{
    "winner": "A" or "B",
    "winner_chapter": N,
    "margin": "clear" or "slight" or "razor-thin",
    "decisive_moment": "决定胜负的引文（来自赢家）",
    "winner_strength": "赢家优势",
    "loser_weakness": "输家短板",
    "best_sentence_a": "A 最佳句",
    "best_sentence_b": "B 最佳句"
}}
"""

BUILD_OUTLINE_SYSTEM = (
        "你把已写成章节反向抽取为结构化大纲。"
        "强调事件、变化、伏笔种下与回收，只输出合法 JSON。"
)

BUILD_OUTLINE_PROMPT = """请分析这一章并输出结构化条目（JSON）。

章节信息：第 {ch} 章《{title_line}》（{wc} 词）

正文：
{text}

返回 JSON，字段：
- title
- location
- characters (list)
- summary（2-3 句）
- beats（3-5 条）
- try_fail（yes-but/no-and/yes-and/no-but）
- plants（本章种下）
- harvests（本章回收）
- emotional_arc
- chapter_question

只输出 JSON。
"""

ARC_SUMMARY_SYSTEM = (
        "你精确概述章节，只写发生了什么、改变了什么、留下什么问题。"
        "不评价，不夸赞。"
)

ARC_SUMMARY_CHAPTER_PROMPT = """请用恰好 3 句话概述本章：
1) 发生了什么
2) 有什么关键变化
3) 章节末留下什么未解问题

章节 {ch}：
{text}
"""

EVAL_SYSTEM = (
        "你是严苛且可执行的小说评估编辑。"
        "所有结论必须可追溯到文本证据，并仅输出合法 JSON。"
)

EVAL_FOUNDATION_PROMPT = """请评估以下小说规划文档（中文）。

VOICE：
{voice}

WORLD：
{world}

CHARACTERS：
{characters}

OUTLINE：
{outline}

CANON：
{canon}

评分维度（0-10）：
magic_system, world_history, geography_and_culture, lore_interconnection, iceberg_depth,
character_depth, character_distinctiveness, character_secrets,
outline_completeness, foreshadowing_balance,
internal_consistency, voice_clarity, canon_coverage

要求：
- 每个维度必须给出 score、gap、fix、note
- 额外输出 slop_in_planning_docs、contradictions_found、overall_score、lore_score、weakest_dimension、top_3_improvements

输出 JSON：
{{
    "magic_system": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "world_history": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "geography_and_culture": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "lore_interconnection": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "iceberg_depth": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "character_depth": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "character_distinctiveness": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "character_secrets": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "outline_completeness": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "foreshadowing_balance": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "internal_consistency": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "voice_clarity": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "canon_coverage": {{"score": N, "gap": "...", "fix": "...", "note": "..."}},
    "slop_in_planning_docs": {{"found": ["..."], "note": "..."}},
    "contradictions_found": ["..."],
    "overall_score": N,
    "lore_score": N,
    "weakest_dimension": "...",
    "top_3_improvements": ["...", "...", "..."]
}}
"""

EVAL_CHAPTER_PROMPT = """请评估以下单章，结合规划文档进行一致性与写作质量检查。

VOICE：
{voice}

WORLD（摘要）：
{world}

CHARACTERS：
{characters}

CANON：
{canon}

本章大纲条目：
{chapter_outline}

上一章结尾：
{prev_chapter_tail}

待评章节：
{chapter_text}

评分维度（0-10）：
voice_adherence, beat_coverage, character_voice, plants_seeded, prose_quality,
continuity, canon_compliance, lore_integration, engagement

要求：
- 每项给出 score 与 note；关键项给 weakest_moment/fix
- 额外输出 three_weakest_sentences, three_strongest_sentences, ai_patterns_detected,
    overall_score, weakest_dimension, top_3_revisions, new_canon_entries

输出 JSON：
{{
    "voice_adherence": {{"score": N, "weakest_moment": "...", "fix": "...", "note": "..."}},
    "beat_coverage": {{"score": N, "weakest_moment": "...", "fix": "...", "note": "..."}},
    "character_voice": {{"score": N, "weakest_moment": "...", "fix": "...", "note": "..."}},
    "plants_seeded": {{"score": N, "weakest_moment": "...", "fix": "...", "note": "..."}},
    "prose_quality": {{"score": N, "weakest_sentence": "...", "fix": "...", "strongest_sentence": "...", "note": "..."}},
    "continuity": {{"score": N, "note": "..."}},
    "canon_compliance": {{"score": N, "violations": ["..."], "note": "..."}},
    "lore_integration": {{"score": N, "weakest_moment": "...", "fix": "...", "note": "..."}},
    "engagement": {{"score": N, "weakest_moment": "...", "fix": "...", "note": "..."}},
    "three_weakest_sentences": ["...", "...", "..."],
    "three_strongest_sentences": ["...", "...", "..."],
    "ai_patterns_detected": ["..."],
    "overall_score": N,
    "weakest_dimension": "...",
    "top_3_revisions": ["...", "...", "..."],
    "new_canon_entries": ["..."]
}}
"""

EVAL_FULL_PROMPT = """请从整本书层面评估小说完成度。

VOICE：
{voice}

WORLD 摘要：
{world_summary}

CHARACTERS：
{characters}

OUTLINE：
{outline}

章节摘要与分数：
{chapter_summaries}

请对以下维度 0-10 打分并说明：
arc_completion, pacing_curve, theme_coherence, foreshadowing_resolution,
world_consistency, voice_consistency, overall_engagement

输出 JSON：
{{
    "arc_completion": {{"score": N, "note": "..."}},
    "pacing_curve": {{"score": N, "note": "..."}},
    "theme_coherence": {{"score": N, "note": "..."}},
    "foreshadowing_resolution": {{"score": N, "note": "..."}},
    "world_consistency": {{"score": N, "note": "..."}},
    "voice_consistency": {{"score": N, "note": "..."}},
    "overall_engagement": {{"score": N, "note": "..."}},
    "novel_score": N,
    "weakest_dimension": "...",
    "weakest_chapter": N,
    "top_suggestion": "..."
}}
"""

ART_STYLE_PROMPT = """你是一名小说美术总监。请基于以下信息定义本书统一视觉风格，并输出 JSON。

小说标题：{title}

WORLD 摘要：
{world}

VOICE 摘要：
{voice}

输出字段：
- art_style
- color_palette
- texture
- mood
- reference_artists
- cover_concept
- ornament_concept
- scene_break_concept
- map_concept

仅输出 JSON。
"""

ART_DIRECTIONS_COVER_PROMPT = """请生成 {n} 个“方向差异极大”的封面视觉方向（JSON 数组）。

风格基线：
- Style: {art_style}
- Palette: {color_palette}
- Mood: {mood}
- Artists: {reference_artists}
- Original: {cover_concept}

每个方向都要明显不同（抽象度、媒介、构图、主体、色彩策略至少变化两项）。
每项字段：direction, concept, medium, prompt。
只输出 JSON 数组。
"""

ART_DIRECTIONS_ORNAMENT_PROMPT = """请生成 {n} 个“方向差异极大”的章节装饰图方案（JSON 数组）。

风格基线：
- Style: {art_style}
- Ornament concept: {ornament_concept}

要求：小尺寸、可用于章节页眉，方向覆盖极简/几何/雕版/具象等差异化路径。
每项字段：direction, concept, medium, prompt。
只输出 JSON 数组。
"""

ART_DIRECTIONS_MAP_PROMPT = """请生成 {n} 个“方向差异极大”的地图视觉方案（JSON 数组）。

风格基线：
- Style: {art_style}
- Map concept: {map_concept}

世界地理摘要：
{world_excerpt}

每项字段：direction, concept, medium, prompt。
只输出 JSON 数组。
"""

ART_DIRECTIONS_SCENE_BREAK_PROMPT = """请生成 {n} 个“方向差异极大”的场景分隔装饰方案（JSON 数组）。

风格基线：
- Style: {art_style}
- Scene break concept: {scene_break_concept}

每项字段：direction, concept, medium, prompt。
只输出 JSON 数组。
"""

AUDIOBOOK_SCRIPT_SYSTEM = (
        "你是有声书脚本拆分编辑。"
        "你把小说拆为可朗读分段，保持说话者归属正确，并仅输出合法 JSON。"
)

AUDIOBOOK_SCRIPT_PROMPT = """请把小说章节解析为有声脚本分段（JSON 数组）。

角色说明：
{characters_json}

音频标签规则：
{audio_tag_guide}

硬规则：
1. 每段都必须有 speaker（叙述为 NARRATOR）
2. 对话去引号
3. 叙述段保持可朗读长度（约 2-4 句）
4. 说话人标签（如“他说”）归入 NARRATOR 段
5. 场景分隔符 --- 转为 {{"speaker": "NARRATOR", "text": "[pause]"}}
6. 第一段输出章节标题朗读
7. 情绪标签克制使用
8. 斜体内心独白归角色本人

章节信息：第 {ch_num} 章《{title}》（{wc} 词）

正文：
{text}

只输出 JSON 数组。
"""
