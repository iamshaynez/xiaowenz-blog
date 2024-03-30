---
title: 大模型的视觉和设计能力。
author: xiaowenz
type: post
date: 2024-03-30T06:00:00+08:00
slug: vision-and-design-by-llm
description: "尝试让 LLM 做出对色彩的判断的过程其实非常有趣，显然，在足够多的语料的堆砌下，大语言模型是可以产生对色彩，色号的「理解」的。"
draft: false
categories:
  - I am a Developer
  - I am a Writer
tags:
  - 社交媒体
  - 人工智能
  - 商业
  - 技术
  - 思考
---

## 背景

[ZenUML](https://zenuml.com) 是我业余时间参与玩耍的一个 Side Project。其功能是定义了一套自己的 DSL，并可以根据代码文本渲染出 UML 中的序列图（Sequence Diagram）。

如下图：

![Sequence Diagram](https://cdn.sa.net/2024/03/30/whIY2s7HAjz4TXu.png)

## 给企业客户的功能

我们在尝试为企业客户自动的提供序列图的配色。

通过读取公司的 logo，官网，甚至只是业务描述，自动的设计出一套专属你的企业的配色主题。

让企业的图表能更好的符合你企业的对外形象，在文档中，宣传中和企业品牌更自然的融为一体。

很自然的，这是一个基于大语言模型 AI 的功能。

## 大语言模型对色彩的理解是基于概率的

尝试让 LLM 做出对色彩的判断的过程其实非常有趣，显然，在足够多的语料的堆砌下，大语言模型是可以产生对色彩，色号的「理解」的。就像从众一般，从统计学上，理论上大语言模型应该可以基于你提供的图片，文本等信息，脑补出让大部分人「统计学上认可」的配色方案。

于是有了如下的交互：

![Poe Bot](https://cdn.sa.net/2024/03/30/L7xRdc3msGzAy9B.png)

## 但概率上有效就是有效

但实际上的效果，其实相当有趣。如下是对不同企业的设计尝试。

**Wendys 连锁快餐**：提供了官网地址，让 LLM 读取后决定应该使用的色彩。

![Wendys Theme](https://cdn.sa.net/2024/03/30/nkyzIKFUGQ5PHxt.png)

**Claude AI**：顶尖大模型 AI 公司，提供了 Logo 让 LLM 决定色彩。

![Claude Theme](https://cdn.sa.net/2024/03/30/7WsFXEwAJNdiRvS.png)

**Nvidia**：算力之王，提供了官网让 LLM 自行决定色彩。

![Nvidia Theme](https://cdn.sa.net/2024/03/30/UTrEIyn1hWHmRDo.png)

**OpenAI ChatGPT**： 提供了Logo，让 LLM 决定色彩。

![OpenAI Theme](https://cdn.sa.net/2024/03/30/lO28ReoiN6U7IMC.png)

**美国运通**：未提供任何信息，利用 LLM 内的知识决定色彩。

![AMEX Theme](https://cdn.sa.net/2024/03/30/A5v4NcYFglP2W7G.png)

**万事达 MasterCard**：未提供任何信息，利用 LLM 内的知识决定色彩。

![Master Card Theme](https://cdn.sa.net/2024/03/30/xFjogZ5aqG91CM7.png)

**Visa**：未提供任何信息，利用 LLM 内的知识决定色彩。

![Visa Theme](https://cdn.sa.net/2024/03/30/kwfyGJjI1zPr64U.png)

## 大语言模型的设计能力

我无法判断大语言模型是否真的有设计上的创新能力，但似乎合理的提示词，至少可以让语言模型算出让人「统计学上认可」的设计方案来。

这也是一种视觉吧？

## 最后

很有趣吧，感谢你读完。