---
title: AI写个代码：Serverless Telegram Bot
author: xiaowenz
type: post
date: 2023-09-21T06:00:00+08:00
slug: serverless-telegram-bot
description: ""
draft: false
categories:
  - I am a Writer
  - I am a Developer
tags:
  - 开发
  - Cloudflare
  - 技术
---

## 最开始

Serverless最大的好处，就是不用操心工程和运行环境，而 Cloudflare 免费的额度，对所有非商用场景，都足够足够了。

计划用 Telegram Bot 作为前端，帮助自己记录一些需要周期性打卡的事儿。作为既没有写过 Worker，也没有用过 D1 的前端苦手，自然是 AI 搭手干活啦。

本程序基于 Serverless 架构的 Cloudflare Worker 和 D1 基于 SQLite 的边缘数据库产品。

![image.png](https://vip2.loli.io/2023/09/21/kbvYLw5Oh1lFnAs.png)

## 开局

起手 Prompt 开局。

```
请使用 Cloudflare Workers 和 Cloudflare D1 数据库，绑定 Telegram Bot，实现一个如下功能的机器人打卡助手。

在 D1 中建立一张 count_log 表，表结构如下：

CREATE TABLE IF NOT EXISTS count_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    count_name TEXT NOT NULL,
    count_type TEXT,
    count_value INTEGER NOT NULL,
    count_date DATE NOT NULL
);


- 机器人接收到的聊天文本信息，进行解析。识别出命令和参数。
- 根据不同的命令，实现不同功能。

### 第一个命令：打卡

会在后台对{内容}这个名词进行一次打卡，记录当天的日期，并返回截止当前打卡的总次数。

例子： 打卡 俯卧撑
输出： 俯卧撑打卡成功，累计打卡 1 次

### 第二个命令：重置打卡

会在后台对{内容}这个名词，重置之前的打卡次数为 0，并记录这一次重置的日期。

例子： 重置打卡 俯卧撑
输出： 重置打卡成功，俯卧撑累计打卡 0 次

### 第三个命令：查询打卡历史

会展示记录过的最近 30 次{内容}这个名字的计数记录，包括重置的记录（如果有）。

例子：查询打卡历史 俯卧撑
输出：
> 俯卧撑 2023-09-01
> 俯卧撑 2023-09-02

请提供完整的代码，对应的工程目录结构。
```

输出的第一版代码：

```javascript
// index.js

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request)) 
})

async function handleRequest(request) {

  if (request.method === 'POST') {
    let body = await request.text()

    let message = JSON.parse(body).message
    let chatId = message.chat.id
    let text = message.text

    let response = await handleCommand(chatId, text)

    return new Response(response, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }

  return new Response('OK')

}

async function handleCommand(chatId, text) {

  let words = text.split(' ')
  let command = words[0]
  let name = words.slice(1).join(' ')

  let responseText

  switch(command) {
    case '/打卡':
      responseText = await countLog(chatId, name, '打卡')
      break
    case '/重置打卡':
      responseText = await resetCount(chatId, name)  
      break
    case '/查询打卡历史':
      responseText = await getHistory(chatId, name)
      break      
    default:
      responseText = '未识别的命令'  
  }

  return JSON.stringify({
    method: 'sendMessage',
    chat_id: String(chatId),
    text: responseText
  })

}

// 连接数据库
const db = D1.table('count_log')

// 打卡
async function countLog(chatId, name, type) {

  let date = new Date().toISOString().slice(0, 10)  

  // 查询今天是否已经打卡
  let result = await db.get(name, date)

  if (result) {
    // 如果今天已经打卡,累加次数
    await db.put(name, date, {
      count_value: result.count_value + 1
    })
  } else {
    // 如果今天还没打卡,插入新记录
    await db.insert({
      count_name: name,
      count_type: type,  
      count_value: 1,
      count_date: date
    })    
  }

  // 查询最新次数
  result = await db.get(name, date)

  return `${name}打卡成功,累计打卡${result.count_value}次`
  
}

// 重置打卡次数
async function resetCount(chatId, name) {
  
  let date = new Date().toISOString().slice(0, 10)

  await db.insert({
    count_name: name,
    count_type: '重置',
    count_value: 0,
    count_date: date
  })

  return `重置打卡成功,${name}累计打卡0次`

}

// 查询打卡历史
async function getHistory(chatId, name) {

  let records = await db.filter(record => record.count_name === name)
                            .sortBy('count_date')
                            .reverse()
                            .limit(30)

  let history = records.map(record => {
    return `${record.count_name} ${record.count_date}`
  }).join('\n')

  return history

}
```

这样，就有了初始版本的代码框架，基本的代码功能（虽然很多 API 其实不能用）。

## 细节功能的例子

具体功能的 Prompt

```
请使用Javascript实现一个解析命令行文本的功能。

要求：

- 接受一个字符串
- 对这个字符串做解析，能识别命令和参数
- 根据不同的命令，调用不同的方法
```

## SQL 编写的例子

写 SQL 的 Prompt

```
SQLite 中有这样一张表

---
CREATE TABLE IF NOT EXISTS count_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    count_name TEXT NOT NULL,
    count_type TEXT,
    count_value INTEGER NOT NULL,
    count_date DATE NOT NULL
);
---

帮我写一个 SQL，统计所有 id 大于最后一个 count_type = 'reset' 的记录的count_value的总和。如果不存在count_type = 'reset'的记录，则返回所有满足条件的记录。
```

## 其余细节

总之，作为一个对 JS 完全不熟悉的人，很快就能构件一个基础功能完备的工程。在没有 AI 的时候，可能需要超过 10 小时摸索才能搞定的小工程，如今 2-3 小时足以。

以下是样例：

![image.png](https://vip2.loli.io/2023/09/21/Fk1dcVQCoem3gJS.png)

## 最后

感谢 Cloudflare，业界良心。免费的提供了足够大部分人构件任何系统的基础设施。