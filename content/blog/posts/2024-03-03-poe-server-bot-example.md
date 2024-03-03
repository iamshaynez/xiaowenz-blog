---
title: 开发一个Poe Server Bot的例子
author: xiaowenz
type: post
date: 2024-03-03T06:00:00+08:00
slug: poe-server-bot-example
description: "距离 ChatGPT 发布所标志着的人工智能卖过金线，已经一年多了。这一年里，借助各方 AI 模型的能力和蛮力，我做了很多过去的自己一定做不到的事儿。"
draft: false
categories:
  - I am a Developer
tags:
  - 社交媒体
  - 人工智能
  - 思考
  - 行业
  - 技术
---

## Poe 是什么

虽然 ChatGPT 是生成式 AI 的领头羊，但我个人的 AI 订阅，过去一年一直是 Quora 旗下的 Poe。因为你可以用同样的订阅费用，使用世界上几乎所有的最新的模型，闭源，开源，都有。

> 详见[Poe](https://poe.com)

## 尝试创建一个 Poe Server Bot 

Poe 提供了可编程的 Server Bot，可以让你更容易的调用所有 Poe 生态里的ChatBot，包括官方提供的模型，和基于官方模型的定制化模型。官方文档在[这里](https://creator.poe.com/)

也就是说，你可以用代码把这些 Bot 作为可随时调用的资源，「串」起一个带有定制逻辑的聊天机器人来。

在通过不同渠道反馈了很多次后，@poe_platform 终于修好了一个很基础的 SDK 问题……我的 Bot 才总算是跑起来了。

## Meme-Creator-Bot

![image.png](https://cdn.sa.net/2024/03/03/F1P3bnuY95IlRvz.png)

尝试创建了一个简单的讲笑话的机器人。这个机器人会根据你提供的任何话题，创作一段 meme quote，并使用画图机器人画一张配图给你。

使用方法很简单，不赘述。

**设计逻辑：**

- 接受用户提供的任何一个「话题」
- 用一个 LLM 来创造一个 meme 的傻句子，并提供一个配合这个句子的图片描述。
- 把图片描述进一步转发到 ImageModel，生成一张图片出来。
- 把这句 meme 和图片都渲染给用户。

**Poe 的优势**

理论上，这个序列里的 LLM 和 ImageModel 可以替换成任何一个 Poe 生态里可调用的模型。

- LLM：GPT3.5，GPT4，Claude, Mistral, Gemini
- Image: StableDiffusionXL, Playground-V2.5, DALLE3

Poe 会根据这个声明，自动计算用户使用这个 Bot 的总成本并扣除使用用户对应的点数。因此，如果按照当前的定价，最贵的是 Claude + DALLE3 的组合。

我当前选择了 Mistral-Large + Playground-V2.5，一共 205 分一次，约等于不要钱。

最终的交互图如下（下面的序列图使用内部未发布的新版 @ZenUML 创建）

![image.png](https://cdn.sa.net/2024/03/03/wqYEPDy7s5Mhb1Z.png)

## 部署 Deployment

Poe 官方推荐使用 Python 语言，并提供了 SDK 更好的集成和部署到 [@modal_labs](https://modal.com/) 。

![image.png](https://cdn.sa.net/2024/03/03/CQ7rS5OAUXKVPHW.png)

因此，本质上可作为无状态的 Serverless Python App 在后台运行，无需开发者自己提供服务器和管理后端资源，很方便。

Modal 提供每个月 30 美元的免费额度，目前看起来可以支撑不小的调用次数，约等于不要钱。

## 最终的效果

如图：

![image.png](https://cdn.sa.net/2024/03/03/ecRZTnNhC6HgfOI.png)

当个有趣的玩具，还是不错的。Poe 最大的优势，还是在于订阅后在一个 Credit 的池子里，让你可以使用到这个世界上大部分的模型，对大部分个人使用者来说，虽然便利性和时效性弱于订阅 ChatGPT Plus，却也提供了更多可能（比如你也许没有 Claude 开发者 API 权限，也不一定想充钱，但 Poe 生态里你已经可以当成所有模型都有 API 调用的能力来构建产品了）。

## 最后

有点啰嗦，感谢你读完。

代码在这里：[https://github.com/iamshaynez/poe-bot-master/blob/main/memes_creator.py](https://github.com/iamshaynez/poe-bot-master/blob/main/memes_creator.py)