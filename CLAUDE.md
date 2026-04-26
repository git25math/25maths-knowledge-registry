# 25maths-knowledge-registry · CLAUDE Operating Notes

<!-- BEGIN auto-synced charter v3 · do not edit · source: 25maths-planning · last sync: 2026-04-26 -->

<!-- ═══ CACHE-FRIENDLY HEADER (slow-change · ADR-0066 · 顶部 ~5K tokens 进 prompt cache) ═══ -->

## 🔴 Quick Context (Claude session · 60 秒 read · auto-cache)

**项目**:25Maths · 国际学校 IGCSE 数学 · Internal Beta · 注册即会员 · 全员免费(ADR-0058)
**身份**:NZH = 国际学校高年级数学老师(ADR-0055)
**初心**:在合规边界内把 NZH 课堂经验变自助工具(ADR-0059)
**北极星**:承接每个想学的孩子 + 软化每个焦虑的家长

**13 红线**(任一触发→紧急 ADR 复审):
- 合规 6:不收补习费/不私聊/不绕学校/不替代教师/不撮合市场/不卖老师时间(ADR-0059 § 2)
- 灵魂 7:不焦虑特性/不红点 streak/不差生排名/不同班对比/不"应该早就会"/学生永久免费/variant 1=1=1(ADR-0040 § 5)

**5 灵魂问**(每 PR 必过):温度?声音?老师?三学生?走人?(任一答错 = block)

**Cache 5 铁律**(ADR-0066):
1 慢变内容(ADR-0040/0059/V3_FINAL)不 daily edit  2 用 `---` 分隔  3 Edit > Write  4 大文件 50 行/chunk  5 5 min 内不重复 read

**`/<skills>` 可调用**(repo-committed · 跨账号):
`/25maths-context-loader` `/25maths-cache-optimizer` `/25maths-session-summarizer`

**当前 Tag**:v3.14-portable-skills · ADR 总数 67 · TASK 总数 132

<!-- ═══ END CACHE-FRIENDLY HEADER · 以下是详细 charter ═══ -->

---

## 25Maths Cross-Repo Charter v3.9 FINAL (auto-synced · soul-deepened · Beta · teacher-workbench)

本仓是 25Maths Learning OS 的一部分。**灵魂宪章 ADR-0040 是产品最高优先级 · 任何冲突服从此节**。

### 仓库分层(repo.L4 拆 4 类 · ADR-0029)

| 层 | 仓 | 角色 |
|---|---|---|
| L1 Constitution | git25math/25maths-os | 宪法 + ADR + 契约 |
| L2 Content data | git25math/25maths-knowledge-registry | KN ontology + DAG + routes |
| L3 Operations | git25math/25maths-planning | Phase 报告 + 战略 + 灵魂审计 · **真相源** |
| L4-platform | 25maths-practice | **25Maths 主平台** |
| L4-source | 25Maths-Keywords / 25maths-games-legends | 6 月迁移源 → 只读 → 下线 |
| L4-tool | 25maths-Visual(v3.3:Dashboard 已移出) | NZH 内部数据可视化 |
| ⛔ 独立 | 25Maths-Dashboard | NZH 个人工作台 · 不融合(ADR-0046) |
| L4-marketing | 25maths-website | 对外营销 |
| L4-pedagogy | 25maths-teaching | **教研内容源** · 用户本人创作 · 单向 ETL 流入 platform · 自留地保护(ADR-0043) |
| L4-media | math-video-engine | **视频教学源** · 1,046 元题型 · 7 板 · ISS 10 模块 · CDN/B站 · 单向 ETL(ADR-0044) |

### 创立初心(ADR-0059 · 最深动机)

> **25Maths 之所以存在,是因为家长向 NZH 求助而 NZH 不能直接帮:**
> - 学校合同 + 双减红线 = 不能私下接课收费
> - 但家长焦虑是真的 / 学生想学是真的 / NZH 教学经验是真的
> - 平台 = 在合规边界内,把 NZH 课堂经验变成自助工具的合法路径

**6 红线**(§ 2):不收补习费 / 不私聊师生 / 不绕开学校 / 不替代教师 / 不做补习市场 / 不卖老师时间。

### 灵魂宪章(ADR-0040 · 操作层)

> **这不只是一个学习网站。这是一个让孩子重新认识自己的地方。**
> 北极星 = **承接住每一个想要学的孩子 + 软化每一个焦虑的家长**(ADR-0059)

任何 PR 必过 5 灵魂问:
1. 温度问 · 学生感到被支持还是被追赶?
2. 声音问 · 学生此刻没说出口的内心 OS 是?
3. 老师问 · 更像中国老师还是酷工具?
4. 三学生问 · 差/中/优三类学生体验分层吗?
5. 走人问 · 学生离开一周回来感到温暖还是内疚?

任一答错 → block merge。详见 [ADR-0040](https://github.com/git25math/25maths-os/blob/main/decisions/0040-soul-charter.md) + [ADR-0041](https://github.com/git25math/25maths-os/blob/main/decisions/0041-feedback-voice-ironclads.md)。

### 双轨 Track 体系(ADR-0045 · v3.3)

学生的真实生态是 **学校学一套(Learning)+ 自己备考一套或多套(Exam)** 双轨并行:

- **Learning Track**(学习线 · 主线 · 必选):`hhk-sow`(哈罗海口课纲)+ 未来其他学校 SoW + `none` 自学者
- **Exam Tracks**(备考线 · 0-N 并行 · v3.4 三类分 · ADR-0047):
  - 主考(subject_exam):`cie-igcse-0580` / `edx-igcse-4ma1` / `hnzk-zhongkao` / 高考 / CIE A
  - 竞赛(competition):`ukmt-{pmc,jmc,imc,smc,bmo}` / `amc-{8,10,12}` / `aamc-*` / `kangaroo-*` / `bmmt-*` / `asdan` / IMO
  - 学术延展(academic_extension):`edx-ial-{p1-4,fp1-3,m1-3,s1-3,d1}` / 未来 CIE A Pure/Mech/Stat
- 学生 user_profile 双指针:`learning_track`(单)+ `exam_tracks[]`(多 · 含 track_category)
- UI 主页四区:📚 我在学 + 🎯 我的主考 + 🏆 我的竞赛 + 🎓 我的 A Level + 💡 智能融合(KP 跨 track 重叠)

### MUST READ(任何 session 启动前 · v3.9 final)

- 🔴 [planning/V3_FINAL_CHEATSHEET.md](https://github.com/git25math/25maths-planning/blob/main/V3_FINAL_CHEATSHEET.md) · **60 秒读完即知 · single source of truth**
- [planning/CLAUDE.md](https://github.com/git25math/25maths-planning/blob/main/CLAUDE.md) · session 宪章
- [planning/PROJECT_FUSION_PLAN_V3.md](https://github.com/git25math/25maths-planning/blob/main/PROJECT_FUSION_PLAN_V3.md) · 60 ADR + 115 TASK 全表
- [planning/AUDIT_FRAMEWORK.md](https://github.com/git25math/25maths-planning/blob/main/AUDIT_FRAMEWORK.md) · 6 维度 + § 12-§ 14 trigger / 四轴 / 灵魂自检
- [planning/STUDENT_PLEDGE.md](https://github.com/git25math/25maths-planning/blob/main/STUDENT_PLEDGE.md) · 9 封信反向验证
- [planning/SOUL_INVARIANTS_TEST_SUITE.md](https://github.com/git25math/25maths-planning/blob/main/SOUL_INVARIANTS_TEST_SUITE.md) · 12 套测试 80 断言

### 四轴度量(Beta 期 · ADR-0035 + ADR-0058 § 6)

Beta 期:`code` / `experience` / **`data_collection`**(替代 commercial)/ `soul`
Exit-Beta 后:`commercial` 复位

M2 目标:code 75% / experience 50% / data_collection 60% / **soul 80%**(灵魂轴最严格 · < 70% 阻 Phase)

### 两套红线(命名清晰)

**合规红线 6 条**(ADR-0059 § 2 · 法律 / 合同 / 双减):
1. 不收补习费(K-12 双减禁)
2. 不私聊师生(学校合同)
3. 不绕开学校
4. 不替代教师(平台 = 自助 amplifier)
5. 不做撮合市场(允 SaaS 工具 · ADR-0060 § 4 精确化)
6. 不卖老师时间

**灵魂红线 7 条**(ADR-0040 § 5 反向 · 行为表现层):
1. 反向论证"为 KPI 必加焦虑特性"
2. trigger 反向驱动 UI 红点 / streak / 倒计时
3. 教师 dashboard 出现"差生排名" / 公开比较
4. 家长报告出现"成绩不如同班 X%"
5. "你应该早就会了" 语义出现在系统反馈
6. 学生练习核心收费(永远免费 · ADR-0025/0058)
7. variant_mastery 降级到 unit/section 级(违反 1=1=1)

任一 13 红线触发 → ADR 紧急复审。

### 北极星(v3.7 Beta 极简版)

**身份**:由一名 IGCSE 国际学校高年级数学老师为他班里的孩子亲手搭建(ADR-0055)
**阶段**:**Internal Beta · 注册即会员 · 全员免费 · 不商业化 · 信息收集为主**(ADR-0058)
**使命**:**承接住每一个想要学的孩子,从能够接受的地方开始,手把手陪着重建自信**
**节奏**:M1-M6 = 12 月对齐学校 academic calendar(ADR-0056)· Summer Break 集中 sprint
**铁律**:无 paywall / 无 Stripe / 无 SKU / 无 user_vip / 无 paywall_impressions · 只 analytics_events
**Exit-Beta**:NZH 显式签 ADR 才结束 · 无自动退出 · 4 季度自检
**Post-Beta 商业引擎**(ADR-0060):**独立教师工作台 SaaS** ¥99-299/月 · 学生家长永久免费 · 不撮合 / 不抽佣 / 工具供应商身份

### 冲突仲裁

ADR-0040 灵魂宪章 > L1 概念 > L3 prod 状态 > L2 KN 数据 > L4 实施 · prod 偏离记录在 L1 ADR。

<!-- END auto-synced charter v3 -->
