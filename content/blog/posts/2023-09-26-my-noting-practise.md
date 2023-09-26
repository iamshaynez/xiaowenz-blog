---
title: 我的笔记实践的变化。
author: xiaowenz
type: post
date: 2023-09-26T06:00:00+08:00
slug: my-noting-practice
description: ""
draft: false
categories:
  - I am a Writer
  - I am a Developer
tags:
  - 思考
  - 逻辑
  - 社交媒体
---

![image.png](https://vip2.loli.io/2023/09/26/1JvgaQusWMBLzGS.png)

最开始接触笔记的时候，应该是看了一个基于 Logseq 的笔记使用的分享。

当时看到的场景大概是这样的：

- 日常记录，习惯性的对一些名词，使用[]符号，创建出一个空连接。
- 之后某一天，我在其他的地方学习到关于这个名词的内容的时候，他们会自然的产生关联
- 之后某一天，我想专题的去写一写关于这个名词的内容的时候，自然可以关联出我所有关于这个内容的笔记来
- 并且有一个看起来很酷炫的「图谱」

于是，很自然的，我被说服了，并开始把印象笔记和 Notion 里的大部分内容，迁移到 Logseq。

而最近一年多，我开始意识到这样的笔记管理和记录的构架，并不能很有效的组织我脑子里的东西，看起来酷炫的图谱，实际上也并没有帮助到我什么。

直到我了解到这：

![image.png](https://vip2.loli.io/2023/09/25/nFDlhPi4qyuSbcT.png)

Evergreen notes： https://notes.andymatuschak.org/About_these_notes?stackedNotes=z5E5QawiXCMbtNtupvxeoEX

Evergreen Notes 的核心仍然基于所谓的卡片笔记法，但是更明确的约定了一些最佳实践：

**1. Evergreen notes should be atomic 笔记应该具有原子性**

> 和大部分的笔记实践一样，一篇笔记只写一件事。值得一提的是，从学习过程的角度，笔记不应该是「摘抄」，你应该至少用你自己的语言，一句话来概括一篇笔记的内容——如果一句话做不到，大概率你需要再拆一次。

**2. Evergreen notes should be concept-oriented 笔记应该基于概念/观念 （而不是名词）**

> 这一条是对我的影响最大的，因为这才是符合知识在大脑里生长的规律的，也符合当我们产生记录的欲望的时候，脑子里大概率出现是基于名词的一些年头，而不是名词本身。

**3. Evergreen notes should be densely linked 笔记之间应该自然的连接起来**

> 减少手工维护笔记之间的关联，或者有能力自动的发现笔记之间的关联，是笔记工具最重要的能力之一了。

**4. Prefer associative ontologies to hierarchical taxonomies 尽量用关联去替代层级管理你的笔记**

> 我曾经在花了很多的脑力在如何物理上设计层级（因为 Obsidian 这样的工具需要你管理文件的层级，Notion 也有这个问题），这并不是人脑需要的。

**5. Write notes for yourself by default, disregarding audience 为自己记笔记，不要考虑受众**

> 这一点，对我个人其实没有啥影响。但很多笔记工具都有类似于直接 Publish 的功能（包括 Notion），于是也许会容易影响写的时候的考量，让人过多的考虑排班，内容，措辞等不必要的东西。

基于这些：我的实践是，笔记基于 Concept，而 Tag 基于名词去连接（类似于 Map of Content 的概念）

**笔记大概是这样：**

![image.png](https://vip2.loli.io/2023/09/25/pQlgT7VGzD3R2hb.png)

**标签大概是这样：**

![image.png](https://vip2.loli.io/2023/09/25/iwM6lYRrWqKmcZn.png)

写了这么多，主要是希望给 @Heptabase 提个需求：

希望提供让 ChatGPT 阅读 Note，然后自动分析出相关的名词并生成 Tag 的能力，实现自动化的笔记在 MoC 角度上的关联的能力。

> 用本地的 Stable diffusion 免费配图真方便啊。