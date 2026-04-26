---
name: 25maths-context-loader
description: Auto-load 25Maths essential context (V3_FINAL_CHEATSHEET + 13 red lines + 5 soul questions + 5 lessons) in cache-friendly order on session start. Cross-account portable (repo-committed). Invoke `/25maths-context-loader` to refresh manually.
---

# 25Maths Context Loader

## 用途
Claude Code 在 25Maths 项目仓内启动 session 时自动 load 这一 skill · 提供以下慢变内容到 prompt 顶部(cache 友好):

## 启动时必须知道(60 秒读完即知)

### 创立初心(ADR-0059 · 永不 archive)
> 25Maths 之所以存在,是因为家长向 NZH(国际学校 IGCSE 数学老师)求助 · 但 NZH 受学校合同 + 双减红线约束不能私下接课 · 平台 = 在合规边界内,把 NZH 课堂经验变自助工具的合法路径。

### 灵魂宪章(ADR-0040 · 最高优先级)
**这不只是一个学习网站。这是一个让孩子重新认识自己的地方。**
北极星 = **承接住每一个想要学的孩子 + 软化每一个焦虑的家长**。

### 13 红线(任一触发 → 紧急 ADR 复审)

**合规红线 6**(ADR-0059 § 2):
1. 不收补习费(K-12 双减禁) 2. 不私聊师生(学校合同) 3. 不绕开学校 4. 不替代教师 5. 不做撮合市场(允 SaaS 工具) 6. 不卖老师时间

**灵魂红线 7**(ADR-0040 § 5):
1. 反向论证"为 KPI 必加焦虑特性" 2. trigger 反向驱动 UI 红点/streak/倒计时 3. 教师 dashboard 出现"差生排名" 4. 家长报告出现"成绩不如同班 X%" 5. "你应该早就会了" 系统反馈 6. 学生练习核心收费(永远免费) 7. variant_mastery 降级到 unit/section 级

### 5 灵魂问(每 PR 必过)
1. 温度问 · 学生感到被支持还是被追赶?
2. 声音问 · 学生此刻没说出口的内心 OS 是?
3. 老师问 · 更像中国老师还是酷工具?
4. 三学生问 · 差/中/优三类学生体验分层吗?
5. 走人问 · 学生离开一周回来感到温暖还是内疚?

### 阶段(ADR-0058)
**Internal Beta · 注册即会员 · 全员免费 · 信息收集为主**
Exit-Beta 后:**独立教师工作台 SaaS** 商业化(ADR-0060 · 学生家长仍永远免费)

### 真相源
- `V3_FINAL_CHEATSHEET.md` · 60 秒可读
- `PROJECT_FUSION_PLAN_V3.md` · 66 ADR + 130 TASK 全表
- `lessons/INDEX.md` · 5 active lessons(同步在 `.claude/skills/25maths-lessons/`)

### NZH / Claude 工作流(ADR-0064)
- L4 永不改:ADR-0040 / 0059
- L3 战略 NZH 必批:ADR-0029/0036/0040/0045/0058/0059/0060
- L2 架构 NZH 简短 review
- L1 可频繁 Claude 自决

### 4 轴度量(Beta 期 · ADR-0058 § 6)
code / experience / **data_collection**(替代 commercial)/ soul

## 触发条件

- **自动**:session 启动时(Claude Code 自动 detect skills/)
- **手动**:用户输入 `/25maths-context-loader` 即重新刷新

## Cross-account 可移植

本 skill 提交 git · 任何 Claude 账号 clone 25maths-planning 即得。
不依赖 user-level memory。

---

## 🔴 FDD 铁律(LESSON-013 哲学根基 · 2026-04-26)

> **后端服务前端 · 前端服务用户 · 后端开发最终点 = 前端更好地为用户服务**

任何 backend TASK 立案前必答 3 问。详见 `lessons/LESSON-013-backend-deploy-is-not-user-experience-ship.md` 核心铁律段。

任何 task 标 ✅ 前必过 DoD 6 步。详见 `AUDIT_FRAMEWORK.md § 7`。
