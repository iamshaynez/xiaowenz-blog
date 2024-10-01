---
title: 一小时自研一个人工智能海龟汤游戏。
author: xiaowenz
type: post
date: 2024-10-01T06:00:00+08:00
slug: turtle-soup-game
description: "Sonnet快速开发在线游戏。"
draft: false
categories:
  - I am a Gamer
  - I am a Developer
tags:
  - 游戏
  - 人工智能
  - 开发
  - 桌游
---

![海龟汤游戏](https://cdn.sa.net/2024/10/01/FkXLJxOqcbjfGRP.png)

## 海龟汤是什么

> 海龟汤的游戏规则，是出题者（煲汤）提出一个令人匪夷所思的事件（汤面），游戏者对出题者进行询问并推理出结局。 游戏者可以提出任何问题，但出题者只能用简单的判断词做出回答，一般而言回答包括四种：是、不是、是也不是、与此无关。

## Poe 上的聊天机器人

很早以前我就在 Poe 上挂了一个海龟汤的游戏，本质上就是把谜题写到提示词里，然后玩家可以和机器人交互，效果还不错。

但 Poe 上最大的问题就是很难分享给喜欢玩的朋友，而且同一时间只能支持一个游戏（故事写进了提示词里）。

## 自己开发一个吧

国庆休假，于是动手自己开发一个吧。需求已经有了，现在就差一个程序员了不是吗？

咱这不是 AI 时代了吗？

**第一段提示词（Sonnet 3.5）：**

```
请帮我写一个一个页面的程序，前后端一体。使用 NodeJS，Html 等技术栈。

功能：

- 前端有一个固定的密码保护，输入密码才能进入
- 前端提供用户一个 ChatBox 的功能，有一个欢迎语。
- 用户在一个 Conversation 中允许不断交互
- Conversation 的内容和后端固定的提示词会一起跟 OpenAI 的 LLM 模型进行交互

请输出给我完整的代码和工程结构
```

于是，你会得到一个初始的版本。这时候的工程量和代码量都不小了，后续要继续修改的话需要有意识的控制上下文。

![Sonnet Coding](https://cdn.sa.net/2024/10/01/mXNCZdjtpBfKn3F.png)

**迭代用的提示词模版（Sonnet 3.5 - 200K）：**

> 使用下面的通用模板，先把当前版本的程序更新进去，然后讲解你需要进一步增加或修改的功能。一次一个，不断迭代。

```
我有一个应用，前端有三个文件：index.html, style.css, script.js，后端一个文件 server.js

功能是一个海龟汤的游戏，用户输入密码进入后，会在一个 Chatbox 内输入问题，后端会和 AI 交互并产生结果返回给前端。

文件内容分别是：

*** 此处省略

---

现在请帮我继续修改：

- 输入密码的页面增加一个文本框，让我展示游戏规则（举例）

```

很快，你就得到了一个画面不丑，功能完整的海龟汤游戏壳子了。

登录界面：

![海龟汤游戏登录](https://cdn.sa.net/2024/10/01/Pje568odAOcQvk3.png)

选择游戏：

![海龟汤游戏选择](https://cdn.sa.net/2024/10/01/bZAjzRDJFwBC1ry.png)

游戏交互：

![海龟汤游戏交互](https://cdn.sa.net/2024/10/01/rUP1swd23AKtjID.png)

## AI的部分

AI 交互的部分其实很简单，就是把玩家输入的信息发到后台，然后跟系统提示词一起发给 LLM 并返回和更新前端页面。

但从游戏体验和经济成本均衡的角度，仍然有几个关键点：

- 要提供尽可能稳定的游戏体验，经过测试，**4o-mini**，**deepseek-2.5** 这一类的廉价快速模型效果并不好，容易出现幻觉并难以对复杂指令做准确的逻辑处理。
- 经过测试，最终我选择的是 **qwen/qwen-2.5-72b-instruct** 和 **meta-llama/llama-3.2-90b-vision-instruct**。这俩属于廉价的价格和介于顶级模型能力和初级模型之间的高水平模型，性价比极高。（阿里和 Meta 都是开源流派，真好。）
- 虽然界面展示的是一个 Conversation，但实际上每次交互只包含一个系统提示词和最新的一个消息，并不会发送历史 Conversation，既可以省钱，也可以提高准确度。
- 模型温度需要降低，幻觉不是游戏引擎希望的。

交互代码如下：

```javascript
  socket.on('chat message', async ({ gameId, message }) => {
    
    try {
      const game = games.find(g => g.id === gameId);
      if (!game) {
        throw new Error('Game not found');
      }

      const response = await openai.chat.completions.create({
        model: process.env.OPENAI_MODEL,
        messages: [
          { role: "system", content: game.systemPrompt },
          { role: "user", content: message }
        ],
        temperature: 0.3,
      });
      socket.emit('chat message', response.choices[0].message.content);
    } catch (error) {
      console.error('Error:', error);
      let errorMessage = 'An error occurred while processing your request.';
      if (error.response) {
        errorMessage += ` Status: ${error.response.status}. ${error.response.data.error.message}`;
      } else if (error.message) {
        errorMessage += ` ${error.message}`;
      }
      socket.emit('error', errorMessage);
    }
  });
```

## 海龟汤游戏体验

体验很好。

世面上能搜到的海龟汤游戏，大多把线下自由度极高的游戏，抽象成了「猜词」或者「做选择题」形式的游戏交互。

基于人工智能的海龟汤游戏，因为自由度极高，基本上可以获得跟真人法官类似的自由体验，毕竟真的什么都可以问。好几个朋友玩的乐此不疲，并有朋友已经独立打完了目前所有的剧本。

> 但也因为是人工智能，所以有很多办法可以 Hack 然后直接通关。不鼓励这么做，毕竟游戏的目标是快乐，而不是获胜不是吗？

