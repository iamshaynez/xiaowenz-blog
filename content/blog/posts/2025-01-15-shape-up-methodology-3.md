---
title: 'Shape Up 阅读笔记（3）- Shaping: 如何真正对需求负责'
author: xiaowenz
type: post
date: 2025-01-15T06:00:00+08:00
slug: shape-up-methodology-3
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

![](https://cdn.sa.net/2025/01/16/FVw3O2A8LWCoycu.png)

大部分软件研发行业说到“增效”，思考的都是怎么让“开发过程”更快。

就像所有的管理问题，从顶层设计才有效一样，所有的效率问题，从最上游找才会出现真正的答案。

Shaping 也许可以给你其中一个优秀的答案。

## Shaping: 如何真正对需求负责

大部分企业，需求分析不过是软件开发流水线中的必要一环。因为大部分的企业，整个流水线上的产品，设计，开发，测试，每一环，都是拿工资干活的工人而已。

![](https://cdn.sa.net/2025/01/15/gr5FNPlIC6RBMqp.png)

> Instead of asking how much time it will take to do some work, we ask: How much time do we want to spend? How much is this idea worth? This is the task of shaping: narrowing down the problem and designing the outline of a solution that fits within the constraints of our appetite.

Shaping 定义的软件需求的思考过程，强制要求先定义价值投入的关系，并只在这个「成本范围内」寻找方案。这意味着如果商业上不值得，在源头上就很难往后流下去，变成浪费资源的垃圾项目。

![](https://cdn.sa.net/2025/01/15/lEFiO2orDdcZIJK.png)

## Shaping 的大致工作流程

- 从一句话的想法「Idea」开始，先进行思考，不要直接渐入任何设计

- 首先思考「appetite」，一个好的点子 idea 很容易让人过度兴奋。需要首先回到真实世界来：我们愿意为此投入多少。

   - 实操上：1-2 weeks or 6 weeks 两种

- 挖掘需求背后准确的问题才能聚焦价值，不要浮于系统功能

- 粗略设计出关键元素

- （以上，是需求分析的过程，以下，是排坑的过程）

- 评估风险，所有标准的评估角度见书本身，和技术专家一起评估可行性。

   - 注意：任何风险评估不到位，都可能导致后续资源极大的浪费

   - 注意：如果后续实施阶段遇到任何不确定性导致的困境，都是 Shaping 阶段的责任

- 最终，把上述关键关键信息，编写成一份叫 Pitch 的文档。

# Pitch 模板

### 问题 Problem

> The raw idea, a use case, or something we’ve seen that motivates us to work on this

### 时间预算 Appetite

> How much time we want to spend and how that constrains the solution

### 方案 Solution

> The core elements we came up with, presented in a form that’s easy for people to immediately understand

### 潜在陷阱 Rabbit Holes

> Details about the solution worth calling out to avoid problems

### 明确排除 No-gos

> Anything specifically excluded from the concept: functionality or use cases we intentionally aren’t cover-ing to fit the appetite or make the problem tractable

## Shaping 的关键原则

-  Shaping 的产出物是一份代表「待办需求」的 Pitch 文档：这份需求最大的特点是：Fixed Time，Variable Scope 时间周期固定，实现程度灵活。

- 不要画原型图，原型图会限制实现的方式，丧失让实施团队自助找到最优解的可能性（边界，边界，边界）

- 从 UI 或者原型图开始设计，很容易掩盖实施阶段的复杂度，因此过度设计更容易导致评估不准，项目逾期。

- 项目不逾期的最佳办法，就是把自由度留给实施团队，只保留最核心的要求和固定的时间窗口。

- 除了约定什么需要做，更重要的是约定哪些是明确不做的，划清边界。


## Shaping 工作需要的专业素养

提出正确，准确的高阶需求，需要非常专业技能：

- 专业产品设计能力

- 业务理解和商业目标，才能准确判断需求的胃口

- 要有能力判断技术可行性：因此不一定需要是开发人员，但一定要真的懂技术


基于上面的要求，很多时候 Shaping 工作需要不止一个人，因为很难有同一个人有所有上述技能。

Shaping 的工作主要是一个产品设计的工作，但比一般的「产品经理」有更大的权利和更高的要求。

## Shaping 工作不是任何项目的一部分

注意，前文提到过，Shaping 工作是和 Building（对应真正的开发实施阶段）同步进行的。Shaping 工作不是任何既有项目的一环，Shaping 工作旨在把商业上的 Idea 转化为 Actionable 的记录，仅此而已。

Shaping 工作本身不含有任何的决策成分，任何 Shaping 的产出物，最终都是很可能不被批准实施的。

但 Shaping 是如此的前置性的工作，他的沉没成本，换来的是避免未来数倍的资源浪费；而所有没有沉没的 Shaping，换来的则是未来开发项目的极大「确定性」和「自由度」。

从任何一个角度来说，在公司的全局视角，Shaping 才是「降本增效」的关键。

而真正决策的过程，叫做 **Betting**，我们下一篇见。

