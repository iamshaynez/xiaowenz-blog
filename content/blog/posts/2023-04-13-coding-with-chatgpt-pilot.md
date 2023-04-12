---
title: 尝试用ChatGPT完整的实现一个Serverless后端工程。
author: xiaowenz
type: post
date: 2023-04-12T13:00:00+08:00
slug: coding-with-chatgpt-pilot
description: "人工智能副驾驶目前并没有降低软件工程的难度和门槛，但确实大大降低了软件实现的难度……"
categories:
  - I am a Developer
tags:
  - 人工智能
  - ChatGPT
  - 思考
  - 软件开发
---

## 写在前面

因为从过年开始，断断续续的开始写一个自己用的记账工具，当时自己的想法是尽量小巧，尽量用自己不熟悉的技术栈来玩。那时候还没有横空出世的ChatGPT，我老老实实的在哄睡张小望的时候看B站的视频把Vue3撸了一遍，然后花了两三天搭了一个前端出来。

后来发现，Cloudflare除了已经有了KV存储外，去年发布了Alpha测试阶段的[D1](https://developers.cloudflare.com/d1) —— 基于SQLite的边缘数据库，于是考虑用Cloudflware Worker和D1来做一个完整的Serverless的后端。

**可我没写过Cloudflare Worker，也没用过SQLite，也不会Javascript。**

> 万事不决问AI，于是有了如下对话：

#### You:
我打算使用Cloudflare Worker + Cloudflare D1的SQLite数据库创建一个后端服务。数据库中会有几张数据库表，Worker提供对这些表的增删改查。请帮忙设计一个基本的代码框架结构，方便后续扩展新的表和新的服务。

#### ChatGPT:
在这个项目中，我们将使用Cloudflare Workers和Cloudflare Durable Objects (D1)的SQLite数据库来创建一个后端服务。为了保持可扩展性，我们将创建一个基本的代码框架结构，以便后续添加新表和新服务。

以下是一个基本的代码框架结构：

1. 文件结构：

```
- src/
  - database/
    - index.js
    - migration.js
  - handlers/
    - index.js
    - table1.js
    - table2.js
  - utils/
    - index.js
  - worker.js
```

2. 代码实现：

/src/database/index.js

```javascript
import { open } from 'sqlite';
import { Database } from 'sqlite3';

export async function getDb() {
  return open({
    filename: ':memory:',
    driver: Database,
  });
}
```

/src/database/migration.js

```javascript
export async function runMigrations(db) {
  await db.migrate({ force: 'last' });
}
```

/src/handlers/index.js

```javascript
import { handleTable1 } from './table1';
import { handleTable2 } from './table2';

export function getHandler(path) {
  switch (path) {
    case '/table1':
      return handleTable1;
    case '/table2':
      return handleTable2;
    default:
      return null;
  }
}
```

/src/handlers/table1.js

```javascript
export async function handleTable1(request, db) {
  // 根据request.method实现对应的增删改查功能
  // 例如: GET, POST, PUT, DELETE
}
```

/src/handlers/table2.js

```javascript
export async function handleTable2(request, db) {
  // 根据request.method实现对应的增删改查功能
  // 例如: GET, POST, PUT, DELETE
}
```

/src/utils/index.js

```javascript
export function parsePath(request) {
  const url = new URL(request.url);
  return url.pathname;
}
```

/src/worker.js

```javascript
import { getDb } from './database';
import { runMigrations } from './database/migration';
import { getHandler } from './handlers';
import { parsePath } from './utils';

addEventListener('fetch', (event) => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const db = await getDb();
  await runMigrations(db);

  const path = parsePath(request);
  const handler = getHandler(path);

  if (!handler) {
    return new Response('Not found', { status: 404 });
  }

  return handler(request, db);
}
```

这个框架为你提供了一个基本的结构，可以根据需要扩展。你可以在`handlers`文件夹下为新表创建新的处理器，并在`handlers/index.js`中将它们添加到路由中。同时，你可以在`database/migration.js`中为新表添加迁移脚本。


#### You:
假设第一张表名为account，字段如下：

#### ChatGPT:
假设`account`表有以下字段：

1. id (整型，主键，自增)
2. username (文本，唯一，不可为空)
3. email (文本，唯一，不可为空)
4. password (文本，不可为空)
5. created\_at (文本，不可为空)
6. updated\_at (文本，可为空)

首先，在`/src/database/migrations`文件夹中创建一个名为`01_create_account_table.sql`的迁移文件：

```
-- /src/database/migrations/01_create_account_table.sql
CREATE TABLE IF NOT EXISTS account (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT
);
```

接下来，修改`/src/database/migration.js`文件，添加迁移文件路径：

```javascript
export async function runMigrations(db) {
  await db.migrate({ force: 'last', migrationsPath: './src/database/migrations' });
}
```

然后，在`/src/handlers`文件夹中创建一个名为`account.js`的文件，实现增删改查功能：

```javascript
// /src/handlers/account.js
export async function handleAccount(request, db) {
  const { method } = request;

  switch (method) {
    case 'GET':
      return getAccounts(db);
    case 'POST':
      return createAccount(request, db);
    case 'PUT':
      return updateAccount(request, db);
    case 'DELETE':
      return deleteAccount(request, db);
    default:
      return new Response('Method not allowed', { status: 405 });
  }
}

async function getAccounts(db) {
  // 查询所有账户
}

async function createAccount(request, db) {
  // 创建新账户
}

async function updateAccount(request, db) {
  // 更新账户
}

async function deleteAccount(request, db) {
  // 删除账户
}
```

最后，在`/src/handlers/index.js`文件中导入并添加新的路由处理程序：

```javascript
import { handleTable1 } from './table1';
import { handleTable2 } from './table2';
import { handleAccount } from './account';

export function getHandler(path) {
  switch (path) {
    case '/table1':
      return handleTable1;
    case '/table2':
      return handleTable2;
    case '/account':
      return handleAccount;
    default:
      return null;
  }
}
```

现在你已经为`account`表创建了对应的增删改查处理程序。你可以按照相同的方法为其他表添加处理程序。


#### You:
请继续实现account.js中的createAccount和getAccounts方法。

#### ChatGPT:
在`account.js`文件中，我们将实现`createAccount`和`getAccounts`方法。为了简化示例，我们不会对密码进行哈希处理，但在实际项目中，你应该使用诸如bcrypt之类的库对密码进行哈希处理。

这是实现`createAccount`和`getAccounts`方法的代码：

```javascript
// /src/handlers/account.js
import { json, text } from 'co-body';

async function getAccounts(db) {
  const accounts = await db.all('SELECT * FROM account');
  return new Response(JSON.stringify(accounts), {
    headers: { 'Content-Type': 'application/json' },
  });
}

async function createAccount(request, db) {
  const requestBody = await json(request);
  const { username, email, password } = requestBody;

  if (!username || !email || !password) {
    return new Response('Missing required fields', { status: 400 });
  }

  const created_at = new Date().toISOString();

  try {
    await db.run(
      'INSERT INTO account (username, email, password, created_at) VALUES (?, ?, ?, ?)',
      [username, email, password, created_at]
    );
  } catch (error) {
    return new Response('Error creating account', { status: 500 });
  }

  return new Response('Account created', { status: 201 });
}
```

在这里，`getAccounts`函数使用`SELECT * FROM account`查询从数据库中获取所有账户，并将结果作为JSON对象返回。

`createAccount`函数首先解析请求正文以获取`username`，`email`和`password`。如果有任何缺失字段，它将返回一个状态为400的响应。然后，它将当前日期和时间作为`created_at`字段的值。接下来，我们尝试将新用户插入到数据库中。如果插入成功，则返回状态为201的响应。如果插入失败，则返回状态为500的响应。

现在你已经实现了`createAccount`和`getAccounts`方法，可以继续实现`updateAccount`和`deleteAccount`方法。请注意，在实际项目中，你可能需要实现更严格的验证和错误处理机制。


#### You:
请问如何在worker.js中输出日志？

#### ChatGPT:
在Cloudflare Workers中，可以使用`console.log()`、`console.info()`、`console.warn()`或`console.error()`方法将日志输出到控制台。这些日志可以在Cloudflare Workers的Dashboard中查看。

在`worker.js`中，你可以在需要的地方添加日志输出，例如：

```javascript
// /src/worker.js
import { getDb } from './database';
import { runMigrations } from './database/migration';
import { getHandler } from './handlers';
import { parsePath } from './utils';

addEventListener('fetch', (event) => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  console.log('Request received:', request);

  const db = await getDb();
  console.log('Database opened');
  
  await runMigrations(db);
  console.log('Migrations run');

  const path = parsePath(request);
  console.log('Request path:', path);
  
  const handler = getHandler(path);

  if (!handler) {
    console.warn('Handler not found for path:', path);
    return new Response('Not found', { status: 404 });
  }

  console.log('Handling request with handler for path:', path);
  return handler(request, db);
}
```

这里，我们添加了一些`console.log()`调用来输出接收到的请求、打开的数据库、运行的迁移以及处理请求的路径。如果找不到请求路径的处理程序，我们还使用`console.warn()`输出一个警告。

要查看这些日志，请在Cloudflare Workers Dashboard中选择对应的Worker，并单击"Logs"选项卡。在这里，你可以实时查看日志输出。请注意，为了查看日志，你需要将Worker部署到开发环境。


#### You:
调试的时候遇到了这个错误。

No matching export in "src/worker.js" for import "default"

#### ChatGPT:
这个错误表明在尝试从`src/worker.js`文件中导入一个名为`default`的导出，但在该文件中找不到匹配的导出。Cloudflare Workers的入口点应该是`addEventListener('fetch', (event) => {})`，而不是一个默认导出。

在你之前提供的`worker.js`文件中，没有使用默认导出，因此你不需要从这个文件中导入默认导出。请确保在其他文件中没有尝试从`src/worker.js`导入默认导出。例如，确保你没有在其他文件中编写类似以下代码：

```javascript
import worker from './worker.js';
```

如果你确实找到了类似的导入语句，请将其删除，因为在`worker.js`文件中已经有了`addEventListener`，你不需要在其他地方导入它。


#### You:
account.js中如何引用util.js里面的方法？

#### ChatGPT:
要在`account.js`中引用`util.js`里的方法，首先需要在`util.js`文件中导出你想要引用的方法，然后在`account.js`中使用`import`语句导入它们。以下是一个示例：

1. 在`/src/utils/index.js`中添加并导出一个名为`yourFunction`的方法：

```javascript
// /src/utils/index.js

export function yourFunction() {
  // 你的函数实现
}
```

2. 在`/src/handlers/account.js`中导入并使用`yourFunction`方法：

```javascript
// /src/handlers/account.js
import { yourFunction } from '../utils';

export async function handleAccount(request, db) {
  // 使用 yourFunction
  yourFunction();

  // 其他代码...
}
```

在这个例子中，我们在`utils/index.js`中定义了一个名为`yourFunction`的函数，并将其导出。然后，在`handlers/account.js`中，我们使用`import`语句导入了`yourFunction`，并在`handleAccount`函数中调用了它。你可以按照这种方式导入和使用任何在`utils/index.js`中定义和导出的函数。


#### You:
请继续实现account.js中的deleteAccount方法。

#### ChatGPT:
接下来，我们将实现`account.js`中的`deleteAccount`方法。这个方法将根据提供的`id`删除相应的账户。

```javascript
// /src/handlers/account.js
import { json, text } from 'co-body';

// ... 其他方法 ...

async function deleteAccount(request, db) {
  const requestBody = await json(request);
  const { id } = requestBody;

  if (!id) {
    return new Response('Missing required field: id', { status: 400 });
  }

  const result = await db.run('DELETE FROM account WHERE id = ?', [id]);

  if (result.changes === 0) {
    return new Response('Account not found', { status: 404 });
  }

  return new Response('Account deleted', { status: 200 });
}
```

在这里，`deleteAccount`函数首先解析请求正文以获取`id`。如果`id`缺失，它将返回一个状态为400的响应。接下来，我们尝试根据`id`从数据库中删除账户。如果找不到匹配的账户（即没有进行任何更改），则返回状态为404的响应。如果删除成功，则返回状态为200的响应。

现在你已经实现了`deleteAccount`方法，可以继续实现其他功能。


#### You:
请确认，Method DELETE的HTTP请求，是否可以包含requestBody

#### ChatGPT:
根据HTTP/1.1规范，`DELETE`方法是可以包含请求正文（request body）的。然而，在实际使用中，大多数情况下，`DELETE`方法不会使用请求正文。相反，通常会将所需的参数作为URL路径参数或查询参数传递。

虽然`DELETE`方法可以包含请求正文，但许多Web服务器、代理和客户端可能不支持它。为了确保更好的兼容性，建议使用查询参数或路径参数来传递所需信息，而不是在`DELETE`请求中包含请求正文。

例如，你可以将之前实现的`deleteAccount`方法修改为使用查询参数传递`id`。这是一个调整后的示例：

```javascript
// /src/handlers/account.js

async function deleteAccount(request, db) {
  const url = new URL(request.url);
  const id = url.searchParams.get('id');

  if (!id) {
    return new Response('Missing required parameter: id', { status: 400 });
  }

  const result = await db.run('DELETE FROM account WHERE id = ?', [id]);

  if (result.changes === 0) {
    return new Response('Account not found', { status: 404 });
  }

  return new Response('Account deleted', { status: 200 });
}
```

这里，我们使用`URL`对象解析请求URL，并从查询参数中获取`id`。然后继续与之前的实现相同的逻辑。现在，你可以在发送`DELETE`请求时使用类似`/account?id=1`的URL来删除具有特定`id`的账户。


#### You:
最后，请帮我实现account.js中的updateAccount方法。方法中要求根据id字段来更新数据，其他字段如果提供了值，就更新，否则不变。

#### ChatGPT:
接下来，我们将实现`account.js`中的`updateAccount`方法。这个方法将根据提供的`id`更新账户的其他字段（如`username`、`email`和`password`），如果提供了新值，则更新，否则保持不变。

```javascript
// /src/handlers/account.js
import { json, text } from 'co-body';

// ... 其他方法 ...

async function updateAccount(request, db) {
  const requestBody = await json(request);
  const { id, username, email, password } = requestBody;

  if (!id) {
    return new Response('Missing required field: id', { status: 400 });
  }

  const existingAccount = await db.get('SELECT * FROM account WHERE id = ?', [id]);
  if (!existingAccount) {
    return new Response('Account not found', { status: 404 });
  }

  const updatedUsername = username || existingAccount.username;
  const updatedEmail = email || existingAccount.email;
  const updatedPassword = password || existingAccount.password;
  const updatedAt = new Date().toISOString();

  try {
    await db.run(
      'UPDATE account SET username = ?, email = ?, password = ?, updated_at = ? WHERE id = ?',
      [updatedUsername, updatedEmail, updatedPassword, updatedAt, id]
    );
  } catch (error) {
    return new Response('Error updating account', { status: 500 });
  }

  return new Response('Account updated', { status: 200 });
}
```

在这里，`updateAccount`函数首先解析请求正文以获取`id`以及其他可选字段。如果`id`缺失，它将返回一个状态为400的响应。接下来，我们尝试从数据库中获取现有账户。如果找不到匹配的账户，则返回状态为404的响应。

然后，我们根据请求中提供的新值更新账户的字段，如果没有提供新值，则使用现有值。我们还将当前日期和时间作为`updated_at`字段的值。接下来，我们尝试更新数据库中的账户。如果更新成功，则返回状态为200的响应。如果更新失败，则返回状态为500的响应。

现在你已经实现了`updateAccount`方法，可以继续实现其他功能。

## 写在最后

受困于AI的知识库版本和限制，上述提供的代码实际上并不能直接使用，缺陷如下：

- 由于即使是现在也没有足够多的D1开发的文档和样例，数据库方面API和处理方式需要自己修正
- Cloudflare Worker目前已经提供了对ES6的集成，关键API有了调整，样例中的也不太成。
- 整个工程结构比较初级，如果希望扩展出更合理的实现方式和细节上的抽象，仍然需要自己动手改很多。

受限于AI的算力（对应一次性可以接受的上下文），实际上很难在一次交互中完整的把所有设计思路都放进去。因此**慢慢拆，慢慢写**会是未来一段时间程序员们对副驾驶协作的常态——一个完整的工程和一块具体的代码实现，中间的抽象信息的数量级至少是百倍的。

**人工智能副驾驶目前并没有降低软件工程的难度和门槛，但确实大大降低了软件实现（从0-0.5）的难度……**

> 以上交互基于ChatGPT4
