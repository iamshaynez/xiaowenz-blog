---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
slug: ""          # 必填：URL 冻结资产 /blog/{slug}.html，^[a-z0-9-]+$；与文件名无关，起好就不要再改
description: ""
tags: []
draft: true       # 推送前删掉本行（lint 把 draft:true 判为「不要推」）
type: blog
---
