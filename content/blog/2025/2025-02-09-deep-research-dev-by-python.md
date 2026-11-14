---
title: "用 AI 写了一个属于自己的 AI Deep Search。"
date: "2025-02-09T19:06:13+08:00"
slug: "deep-research-dev-by-python"
description: "不断补充的例子(持续更新留档) 小米汽车全球汽车行业北极星指标对标及战略分析报告 中国信用卡消费市场综合分析报告(2015-2030) 微信R1搜索整合对内容生态的战略影响评估报告 背景 OpenAI 的 Deep Search 功能发布后..."
tags:
  - "technology"
draft: false
type: "blog"
---

![Deep Search](https://cdn.sa.net/2025/02/09/u7ARWveNC89rUhF.png)

## 不断补充的例子(持续更新留档)

- [小米汽车全球汽车行业北极星指标对标及战略分析报告](/research/xiaomi-auto-strategy-report-deep-research)
- [中国信用卡消费市场综合分析报告(2015-2030)](/research/china-credit-card-market-deep-research-analysis)
- [微信R1搜索整合对内容生态的战略影响评估报告](/research/wechat-r1-deep-research-search-strategy-analysis)

## 背景

OpenAI 的 Deep Search 功能发布后，很多人打呼「一个月 200刀太值了」。

在比较了几个 Deep Search 产出的报告后，也参考了诸如 GPT-Research 等工具的工作思路后，发现这事儿似乎并不应该这么「昂贵」。

## 拍脑袋设计

设计很简单：

- 让 AI 自己想清楚研究主题，并生成一个研究计划。
- 然后执行这个计划，收集资料文献
- 然后整理和读取这些文献，生成报告

下图是 GPT Researcher 的设计

![GPT Researcher 的设计](https://cdn.sa.net/2025/02/09/56Bu7vV8fesmg9k.png)

## 落地设计

落地会稍微复杂一点，因为要解决一些实际上的困难，如 Token 的限制，比如网上中文信息和英文信息质量差异等，比如各类不同 AI 模型的表现稍微不同。

于是增加了：

- 先把用户 Query 翻译成英文，以便所有信息来源使用英文世界的
- 因为无论是 AI 调用还是搜索都使用付费接口，所以过程数据需要持久化，以便「断点续传」，节约成本。
- 不同的场景使用不同的 AI，降低成本
- 材料需要先一次汇总和梳理，降低幻觉
- 最终输出的报告使用的语言用户可以指定

![Design](https://cdn.sa.net/2025/02/09/3UPtxEc6eDK4RvA.png)

## 实现

- 95% 的代码由字节国际发布的 Trae AI Coding IDE 完成。
- 但需要自己设计模块，并按照模块，一块一块的用提示词指导，不可能一蹴而就。
- 看了一下历史，交互大概三十来次而已。
- Trae 当前免费，使用 Sonnet 3.5，免费的就是无敌。

![Trae](https://cdn.sa.net/2025/02/09/ozENhaij7xCIZ5r.png)

- 最终，AI 网关使用 OpenRouter 家的，因为需要 Gemini 的 2M 上下文能力。思考和编写使用 DeepSeek-R1，每次报告总成本大概 1.5 人民币左右。
- 搜索使用 Tavily，每月免费 1000 个 Token，每个报告平均需要 100 个 Token，折合人民币 5 元左右。

## 例子

- [中国银联业务深度量化分析报告](/%E4%B8%AD%E5%9B%BD%E9%93%B6%E8%81%94%E4%B8%9A%E5%8A%A1%E6%B7%B1%E5%BA%A6%E9%87%8F%E5%8C%96%E5%88%86%E6%9E%90%E6%8A%A5%E5%91%8A.pdf)
- [深度解析DeepSeekR1技术生态系统下的中国A股投资机遇](/%E6%B7%B1%E5%BA%A6%E8%A7%A3%E6%9E%90DeepSeekR1%E6%8A%80%E6%9C%AF%E7%94%9F%E6%80%81%E7%B3%BB%E7%BB%9F%E4%B8%8B%E7%9A%84%E4%B8%AD%E5%9B%BDA%E8%82%A1%E6%8A%95%E8%B5%84%E6%9C%BA%E9%81%87.pdf)

## 最后

鞠躬感谢 AI 时代。

~~还在整理和拓展代码，晚些才能开源出来（现在还在 IDE 里面跑）。~~

## 代码

[GitHub - iamshaynez/deep-research-cli

Contribute to iamshaynez/deep-research-cli development by creating an account on GitHub.

![https://github.com/iamshaynez/deep-research-cli](https://github.githubassets.com/favicons/favicon.svg)github.com

![GitHub - iamshaynez/deep-research-cli](https://opengraph.githubassets.com/17c35dd58f06cc259819aa5989c6a45b9b15010e1acbc7dc7c858c3a2d6b480e/iamshaynez/deep-research-cli)](https://github.com/iamshaynez/deep-research-cli)
