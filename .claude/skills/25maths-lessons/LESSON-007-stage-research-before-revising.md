---
name: 多 stage 研究先做 inventory · 再下结论
description: Stage 5-7 研究中发现 v3 plan 已覆盖 Stage 5 多数 gaps · 若未先 inventory 会重复造 4 个新 TASK
type: feedback
auto_load: true
---

# LESSON-007 · 多 stage 研究先做 inventory · 再下结论

## 触发场景

2026-04-26 Stage 8 SYNTHESIS 起草过程:

1. Claude 读 Stage 5 RESEARCH(17 gaps)→ 第一版 SYNTHESIS 提议加 4 个新 TASK(021/022/023/024)
2. NZH 同意继续推进
3. Claude 写 v3 plan 发现 TASK-021/022/024 **已存在不同含义** · 编号冲突
4. Claude 改用 TASK-137/138/139 后 · 再 grep · 发现 TASK-025(课堂 schema · Gap H)+ TASK-027(人教课标 · Gap K)**已经在 v3 plan**
5. 最终 4 个 "新" TASK → 实际只 1 个真正新(TASK-137 · 教学铁律)
6. 节省 NZH 工作量 1.5-2d

## 问题

**若不先 inventory · 会重复造轮子**:
- 多个 TASK 编号冲突 · 浪费命名空间
- gap 分类后才发现 v3 已覆盖 · SYNTHESIS 文档需要重写
- 给 NZH 的"待办清单"虚高 · 失信任

## 规则

**Why**:Stage 综合不是新 TASK 工厂 · 是"v3 plan 已覆盖度审计"。多数 stage 发现的 gap 应已在某个 TASK 描述里 · 重新发明 = LESSON-001 类型错误。

**How to apply**:
1. 写 SYNTHESIS 之前 · 先 `grep -E "TASK-[0-9]+" PROJECT_FUSION_PLAN_V3.md | sort -u` 看现有编号
2. 每个 gap 先在 v3 plan 用关键词 grep · 确认是否已有对应 TASK
3. 只有 grep 无结果的 gap 才提"新 TASK"
4. SYNTHESIS § "已存在不重复" 章节 必备 · 显示给 NZH "我已 inventory 过"
5. 新 TASK 编号必须用 `grep -oE "TASK-[0-9]+" | sort -u | tail -1` 后 +1

## 反例(2026-04-26)

```
第一版 SYNTHESIS:
  - 加 TASK-021 (实际已是 get_section_health)
  - 加 TASK-022 (实际已是 L2 加 ikp_id)
  - 加 TASK-023 (用 ✅ 但用了 023 这个未确认编号)
  - 加 TASK-024 (实际已是 exam_boards 注册表)

第二版修正:
  - 加 TASK-137 / 138 / 139(用 max+1 后空号)

第三版 grep 后:
  - 仅 TASK-137 是真新(教学铁律)
  - Gap H → TASK-025 已在
  - Gap K → TASK-027 已在
  - Gap C/E/O → TASK-024 已在
```

## 同类 LESSON 关联

- LESSON-001:awk 多行失败 · 用 Python 替换 · 类似"先 inventory 再实施"
- LESSON-005:不要无条件加新功能 · 先验证是否已有
