---
title: 'Shape Up 阅读笔记（7）- 还有些重要的细枝末节'
author: xiaowenz
type: post
date: 2025-01-19T06:00:00+08:00
slug: shape-up-methodology-7
description: ""
draft: false
categories:
  - I am a Developer
  - I am a Reader
tags:
  - 阅读
  - 书单
  - 管理
  - 软件研发
  - 思考
---

![](https://cdn.sa.net/2025/01/20/5LvTPI1cqxasznW.png)

# 关于 QA 的定位（边缘场景 only）

- QA 在每个 Cycle 的尾声进入，并测试各种边缘场景

- 实施团队对主要功能的质量负责

- Basecamp 的实践是，很多年来都没有 QA 这个角色，直到业务的规模发现，边缘场景的 bug 造成的影响足够大了

- QA 是 Level-up（增值），而非 Check-point（兜底）

- QA 提交的 tasks 默认是 nice-to-have 属性，实施团队来决定是否要修复

# 关于 Code Review

- Code Review 和 QA 测试一样，不是强制的

- Code Review 会让代码变得更好，但不强制

- Code Review 是 Teaching 和 Learning 的机会，应该珍惜抓住而非逃避

# 如何对待线上发现的 Bugs

- 首先，真实的考虑 bugs 的影响。大部分的 bug 可以等六周或者不需要修。

- 处置：

   - 用 cool down

   - 用 betting table，正式的

   - 偶尔安排专门的 bug smash 周期，某个六周只修 bug

# 关于项目延期的原则

- 极少的项目允许延期

- 所有遗留的没有做完的 Tasks，都是确实是 must-have 的

- 剩余的 Tasks 必须是 downhill 状态的，没有不确定性，没有未解答的问题

- 即使如此，大部分项目我们仍然不鼓励延期

- 2 weeks 的 Cool Down 可用来完成未完成的项目，但不鼓励，不应该是常态

- 任何未完成的项目中，如果有 uphill 状态的工作，都被视为 shaping  本身的问题。任何带有不确定性的项目，都应该回到 shaping 阶段去重新探讨，直到重新完善后通过同样的 Betting 过程，回到未来的某个 Cycle 中

# Pitches 是如何被管理的

- 所有写好初稿的 Pitches 会被发送到一个专门的频道里，异步评审

- 所有 stakeholder 自行阅读

- 异步的 comment 并尽可能修正，解决所有的顾虑

- 因此这个 Shaping 的过程，是同样值得和 Cycle 等价6 周的

- 绝不在评审阶段说 yes or no（这是 betting 做的），这是重要的边界

- 但所有的 Idea，默认的态度都应该是： no，值到它被足够的思考，最终塑造成赌桌上值得下注的筹码

- 所有没有被批准的 Pitch，都等同于作废。除非显著的被修改后重新提起。（注意重申：没有任何 Backlog）

## 特殊的超大型项目怎么操作？

书内有从 0-1 一个产品，显然 6 周不可能做完的场景。详细的见书中原文，但个重点很有意思：

- 会有一个特殊的初期（R&D Mode），这个阶段工作节奏仍然和 Cycle 一样，但 Pitch 和分工均有不同。

   - Pitch 可以允许写的比较模糊，因为很多事需要在建设的过程中才能学习到

   - 尽量不给标准的实施团队，而是资深的管理层（CTO 哟）亲自先做。原因如下两个：

      - 当你自己都不知道要什么的时候，你无法让别人来做，这是不负责任的表现

      - 架构责任极大，需要高层级的人来担

   - 最终这个阶段产出的是基础的设计和代码，不一定是可 ship 到市场的可用版本，但决定了整个产品的可行性，未来产品的大致形态等


> **至此，所有《Shape Up》这本书的内容，我都重新串了一次，希望对您有帮助。**


