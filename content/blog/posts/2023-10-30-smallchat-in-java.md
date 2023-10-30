---
title: 70行代码实现一个简单的聊天室。
author: xiaowenz
type: post
date: 2023-10-30T06:00:00+08:00
slug: smallchat-in-java
description: ""
draft: false
categories:
  - I am a Developer
tags:
  - 技术
  - sideproject
  - 爱好
---

![Program is a small thing](https://vip2.loli.io/2023/10/30/7Maq6l41AwmrEG8.png)

## Salvatore Sanfilippo 的 Chatroom

Redis 作者 Salvatore Sanfilippo 最近创建一个新的演示项目：smallchat，用了200行代码(C语言)实现了一个聊天室。

**仓库地址：** https://github.com/antirez/smallchat

**README 如下：**

```
TLDR: This is just a programming example for a few friends of mine. Long story follows.

Yesterday I was talking with a few friends of mine, front-end developers mostly, that are a bit far from system programming. We were remembering the old times of IRC. And inevitably I said: to write a very simple IRC server is an experience everybody should do. There are very interesting parts in a program like that. A single process doing multiplexing, taking the client state, that can be done in different ways, and so forth.

But then the discussion evolved and I thought, I'll show you a very minimal example in C. But what is the smallest chat server you can write? For starters to be truly minimal we should not require any proper client. Even if not very well, it should work with telnet or nc (netcat). The server main operation is just to receive some chat line and send it to all the other clients, in what is sometimes called a fan-out operation. But yet, this would require a proper readline() function, then buffering, and so forth. We want it simpler: let's cheat using the kernel buffers, and pretending we every time receive a full-formed line from the client (an assumption that is in the practice often true, so things kinda work).

Well, with this tricks we can implement a chat that even has the ability to let the user set their nick in just 200 lines of code (removing spaces and comments, of course). Since I wrote this little program as an example for my friends, I decided to also push it here on Github.
```

**翻译：（ChatGPT 翻译）**

```
摘要：这只是我为几位朋友编写的一个编程示例。事情是这样的：

昨日我与几位朋友交谈，他们主要是前端开发者，与操作系统领域的编程还有些距离。我们回忆起使用IRC的老时光。我说过：每个人都应该尝试去编写一个非常简单的IRC服务器。在这样的程序中，有很多非常有趣的部分。一个单独的进程进行多路复用，处理客户端状态，这可以通过不同的方式完成，等等。

然而，随着讨论的深入，我想，我将给你们展示一个用C语言编写的最简单的例子。但是，你能写出最小的聊天服务器是什么样的呢？首先，为了真正的小巧，我们应该不需要任何专门的客户端。即使效果不是很好，它也应该能够使用telnet或nc（netcat）。服务器的主要操作就是接收一些聊天行并将其发送给所有其他客户，这在有时被称为扇出操作。然而，这仍然需要一个恰当的readline()函数，然后是缓冲，等等。我们希望它更简单：让我们使用内核缓冲区来作弊，并假设我们每次都从客户端接收到一个完全形成的行（这在实践中常常是真实的，所以事情也就能够运作）。

嗯，通过这些技巧，我们甚至可以实现一个允许用户设置他们昵称的聊天程序，只需要200行代码（当然，去掉空格和注释）。因为我为我的朋友们写了这个小程序作为示例，我决定也在Github上发布。
```

## Go 语言的版本

于是，@Smallnest 写一个 Go 语言的版本。

地址：https://github.com/smallnest/smallchat

![image.png](https://vip2.loli.io/2023/10/30/WRUz4d9lTcCeIQi.png)

代码行数为 90。

## Java 语言的版本

于是，作为老派的 Java 选手，我写了一个 Java 的版本。其实，甚至工作中自己都有好些时间没有系统性的写 Java 代码了，但发现，有一些最基本的愉悦，其实是相通的。

还记得在大学的时候，操作系统这门课的课后作业，就是在最基本的环境里，实现一个内存里的 DOS 操作系统。用最原始的方法，在内存中实现文件的分片管理，这种最底层的实践，如今成为了我大学期间写过的所有代码里，唯一记住的东西。

所以看到这个用最基本的 socket 实现玩具的小项目，趁着孩子睡了，赶紧动手一波。这个项目是用 Java 实现的类似功能。

地址：https://github.com/iamshaynez/ChatRoom

代码行数：78。

## 最后

权当一笑，感谢您读完。