# xiaowenz-blog

## Host server with bind for testing new page or post from external

```
hugo server --bind="0.0.0.0" -D
hugo new blog/posts/my-first-post.md
hugo new blog/weekly/my-first-post.md
```

## New Post Header Template

```
---
title: "test"
date: 2022-08-15T13:45:17+08:00
draft: true
author: xiaowenz
type: post
slug: test
description: "xxx……"
categories:
  - I am a Writer
tags:
  - 周报
  - 辛苦
---
```



