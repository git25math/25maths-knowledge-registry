# 25maths-knowledge-registry · CLAUDE Operating Notes

<!-- BEGIN auto-synced charter v3 · do not edit · source: 25maths-planning · last sync: 2026-04-25 -->

## 25Maths Cross-Repo Charter v3 (auto-synced · soul-deepened)

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

### 灵魂宪章(产品最高优先级)

> **这不只是一个学习网站。这是一个让孩子重新认识自己的地方。**
> 北极星 = **承接住每一个想要学的孩子**

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

### MUST READ(任何 session 启动前)

- [planning/CLAUDE.md](https://github.com/git25math/25maths-planning/blob/main/CLAUDE.md) · session 宪章
- [planning/PROJECT_FUSION_PLAN_V3.md](https://github.com/git25math/25maths-planning/blob/main/PROJECT_FUSION_PLAN_V3.md) · § -1 灵魂 + § 1 战略 + § 11 自检
- [planning/AUDIT_FRAMEWORK.md](https://github.com/git25math/25maths-planning/blob/main/AUDIT_FRAMEWORK.md) · 6 维度 + § 12-§ 14 trigger / 四轴 / 灵魂自检
- [planning/STUDENT_PLEDGE.md](https://github.com/git25math/25maths-planning/blob/main/STUDENT_PLEDGE.md) · 9 封信反向验证
- [planning/SOUL_INVARIANTS_TEST_SUITE.md](https://github.com/git25math/25maths-planning/blob/main/SOUL_INVARIANTS_TEST_SUITE.md) · 12 套测试 80 断言

### 四轴度量(M2 末目标 · ADR-0035 + ADR-0040)

code 75% / experience 50% / commercial 20% / **soul 80%**(灵魂轴最严格 · < 70% 阻 Phase)

### 7 红线(违反任一 → ADR-0040 紧急复审)

1. 反向论证"为 KPI 必加焦虑特性"
2. trigger 反向驱动 UI 红点 / streak / 倒计时
3. 教师 dashboard 出现"差生排名" / 公开比较
4. 家长报告出现"成绩不如同班 X%"
5. "你应该早就会了"语义出现在系统反馈
6. 学生练习核心收费(ADR-0025 学生永远免费)
7. variant_mastery 降级到 unit/section 级(违反 1=1=1 铁律)

### 北极星(双锚)

商业:DFM-killer + Y3 ¥1 亿 + 6 月渐进融合
使命:**承接住每一个想要学的孩子,从能够接受的地方开始,手把手陪着重建自信**

### 冲突仲裁

ADR-0040 灵魂宪章 > L1 概念 > L3 prod 状态 > L2 KN 数据 > L4 实施 · prod 偏离记录在 L1 ADR。

<!-- END auto-synced charter v3 -->
