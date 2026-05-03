---
name: Supabase 列名必须以 prod migration 为准 · 错列触发 400 + 11s click hang + auth lock steal
date: 2026-05-03
type: workflow
auto_load: true
---

# LESSON-027 · Supabase 列名验证铁律

## 事故

`src/pages/teacher/LessonGrade.tsx:88` 写:

```ts
supabase.from('kw_class_students').select('user_id, display_name').eq('class_id', classId)
```

`kw_class_students` 实际列是 `student_name`(prod migration `20260402_legacy_surface_lockdown.sql:198` `INSERT INTO public.kw_class_students (class_id, user_id, student_name)`),不是 `display_name`。

### 连锁后果(浏览器 console 实测)

1. PostgREST 返回 **400 Bad Request**
2. 调用方 `Promise.all([...])` 没 catch → unhandled rejection 阻塞
3. **'click' handler took 11567ms** ← 学生肉眼可见的"点了没反应"
4. supabase-js auth lock `lock:sb-...-auth-token` 5s 超时被 `getUser()` 抢占
5. 报错 `Lock was released because another request stole it` 连锁触发 `TeachingUnits` 白屏

## 根因

- 同表其他 6 处调用都用 `student_name`(CurriculumBoardPanel / ExitTicketDashboard / GrowthTimeline / LiveBoardPanel / StudentReport / ErrorTargetedAssembler)
- 仅 `LessonGrade.tsx` 一处错,grep `display_name` 立刻定位,arc 改 1 行修
- `tsc` 不能抓 — supabase-js 的 `.select(string)` 是 string literal,prod schema 不在编译期视野

## 铁律

1. **写 supabase 查询前必 grep prod migration**:`grep -rn "CREATE TABLE.*<table>\|INSERT INTO.*<table>" supabase/migrations/` 确认实际列名
2. **同表多处调用时优先 grep 既有用法**:`grep -rn "from('<table>')" src/` 看 5 个文件用 A,1 个用 B → B 99% 是错的
3. **400 + 长 click handler + auth lock steal 三连症 = 列名/RLS 错**:不要先怀疑网络/锁/race,先 grep schema
4. **Promise.all 含 supabase 查询必 catch 单查询**:否则 1 个 400 阻塞整个 await 链 → click handler 飙到 10s+
5. **教师端跨表查询是高发区**:学生侧通常自查 `auth.uid()`,教师侧跨 `kw_classes` / `kw_class_students` / `student_*` 多表 join,列名错最易藏

## How to apply

- 新增 / 改 supabase 查询前 30s 自查:① migration 列名 ② 同表 grep 既有用法 ③ Promise.all 单查询 catch
- 用户报"点了卡住" + console 有 400 → 直接 grep 错列,不要先 profile / lock 调试
- LESSON-010(grep prod schema not just frontend code)的前端代码层落地版

## 相关

- 修复 commit: `25maths-practice@128bcdfed` (2026-05-03)
- LESSON-010 schema 域 · LESSON-013 backend ≠ ship · LESSON-017 pre-ship 7 bug
