# fastzdp_sqlmodel

基于SQLModel封装的专用于FastAPI处理MySQL数据库业务的框架

Github开源地址：https://github.com/zhangdapeng520/fastzdp_sqlmodel

## 安装

```bash
pip install fastzdp_sqlmodel
```

## 使用教程

### 创建表

```python
from typing import Optional
from sqlmodel import Field, SQLModel
import fastzdp_sqlmodel as fsqlmodel


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


# 创建数据库引擎
engine = fsqlmodel.get_engine(database="fastzdp_sqlmodel")

# 删除所有表
SQLModel.metadata.drop_all(engine)

# 创建所有表
SQLModel.metadata.create_all(engine)
```

### 添加数据

```python
from typing import Optional
from sqlmodel import Field, SQLModel
import fastzdp_sqlmodel as fsqlmodel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


# 创建数据库引擎
engine = fsqlmodel.get_engine(database="fastzdp_sqlmodel")
fsqlmodel.init_table(engine)

# 创建数据
u = User(name="张三", age=23)
fsqlmodel.add(engine, u)
```

### 查询所有数据

```python
from typing import Optional
from sqlmodel import Field, SQLModel
import fastzdp_sqlmodel as fsqlmodel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


# 创建数据库引擎
engine = fsqlmodel.get_engine(database="fastzdp_sqlmodel")

# 初始化表格
fsqlmodel.init_table(engine)

# 创建数据
u = User(name="张三", age=23)
fsqlmodel.add(engine, u)
u = User(name="李四", age=24)
fsqlmodel.add(engine, u)

# 查询所有数据
users = fsqlmodel.get_all(engine, User)
print(users)
```

### 根据字典查询数据

```python
from typing import Optional
from sqlmodel import Field, SQLModel
import fastzdp_sqlmodel as fsqlmodel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


# 创建数据库引擎
engine = fsqlmodel.get_engine(database="fastzdp_sqlmodel")

# 初始化表格
fsqlmodel.init_table(engine)

# 创建数据
u = User(name="张三", age=23)
fsqlmodel.add(engine, u)
u = User(name="张三", age=24)
fsqlmodel.add(engine, u)
u = User(name="李四", age=24)
fsqlmodel.add(engine, u)

# 查询所有数据
query = {"name": "张三"}
users = fsqlmodel.get_by_dict(engine, User, query)
print(users)
```

### 逻辑 or 查询

```python
from typing import Optional
from sqlmodel import Field, SQLModel
import fastzdp_sqlmodel as fsqlmodel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


# 创建数据库引擎
engine = fsqlmodel.get_engine(database="fastzdp_sqlmodel")

# 初始化表格
fsqlmodel.init_table(engine)

# 创建数据
u = User(name="张三", age=23)
fsqlmodel.add(engine, u)
u = User(name="张三", age=33)
fsqlmodel.add(engine, u)
u = User(name="李四", age=24)
fsqlmodel.add(engine, u)

# 查询年龄等于23或者小于10的用户
query = {"age": {">": 23, "<": 10}}
users = fsqlmodel.get_by_dict_or(engine, User, query)
print(users)
```

### 逻辑 and 查询

```python
from typing import Optional
from sqlmodel import Field, SQLModel
import fastzdp_sqlmodel as fsqlmodel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


# 创建数据库引擎
engine = fsqlmodel.get_engine(database="fastzdp_sqlmodel")

# 初始化表格
fsqlmodel.init_table(engine)

# 创建数据
u = User(name="张三", age=23)
fsqlmodel.add(engine, u)
u = User(name="张三", age=33)
fsqlmodel.add(engine, u)
u = User(name="李四", age=24)
fsqlmodel.add(engine, u)

# 查询年龄等于20或者小于30的用户
query = {"age": {">": 20, "<": 30}}
users = fsqlmodel.get_by_dict_and(engine, User, query)
print(users)
```

### 根据ID查询

```python
from typing import Optional
from sqlmodel import Field, SQLModel
import fastzdp_sqlmodel as fsqlmodel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


# 创建数据库引擎
engine = fsqlmodel.get_engine(database="fastzdp_sqlmodel")

# 初始化表格
fsqlmodel.init_table(engine)

# 创建数据
u = User(name="张三", age=23)
fsqlmodel.add(engine, u)
u = User(name="张三", age=33)
fsqlmodel.add(engine, u)
u = User(name="李四", age=24)
fsqlmodel.add(engine, u)

# 查询id为1的数据
u = fsqlmodel.get(engine, User, 1)
print(u)

# 查询id为11的数据
u = fsqlmodel.get(engine, User, 11)
print(u)
```

### 修改数据

```python
from typing import Optional
from sqlmodel import Field, SQLModel
import fastzdp_sqlmodel as fsqlmodel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


# 创建数据库引擎
engine = fsqlmodel.get_engine(database="fastzdp_sqlmodel")

# 初始化表格
fsqlmodel.init_table(engine)

# 创建数据
u = User(name="张三", age=23)
fsqlmodel.add(engine, u)

# 查询id为1的数据
u = fsqlmodel.get(engine, User, 1)
print(u)

# 修改
update_dict = {"name": "张三333"}
fsqlmodel.update(engine, u, update_dict)

# 查询id为1的数据
u = fsqlmodel.get(engine, User, 1)
print(u)
```

### 根据ID修改数据

```python
from typing import Optional
from sqlmodel import Field, SQLModel
import fastzdp_sqlmodel as fsqlmodel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


# 创建数据库引擎
engine = fsqlmodel.get_engine(database="fastzdp_sqlmodel")

# 初始化表格
fsqlmodel.init_table(engine)

# 创建数据
u = User(name="张三", age=23)
fsqlmodel.add(engine, u)

# 查询id为1的数据
u = fsqlmodel.get(engine, User, 1)
print(u)

# 修改
update_dict = {"name": "张三333"}
fsqlmodel.update_id(engine, User, 1, update_dict)

# 查询id为1的数据
u = fsqlmodel.get(engine, User, 1)
print(u)
```

### 删除数据

```python
from typing import Optional
from sqlmodel import Field, SQLModel
import fastzdp_sqlmodel as fsqlmodel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


# 创建数据库引擎
engine = fsqlmodel.get_engine(database="fastzdp_sqlmodel")

# 初始化表格
fsqlmodel.init_table(engine)

# 创建数据
u = User(name="张三", age=23)
fsqlmodel.add(engine, u)

# 查询id为1的数据
u = fsqlmodel.get(engine, User, 1)
print(u)

# 删除
fsqlmodel.delete(engine, u)

# 查询id为1的数据
u = fsqlmodel.get(engine, User, 1)
print(u)
```

### 根据ID删除数据

```python
from typing import Optional
from sqlmodel import Field, SQLModel
import fastzdp_sqlmodel as fsqlmodel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None


# 创建数据库引擎
engine = fsqlmodel.get_engine(database="fastzdp_sqlmodel")

# 初始化表格
fsqlmodel.init_table(engine)

# 创建数据
u = User(name="张三", age=23)
fsqlmodel.add(engine, u)

# 查询id为1的数据
u = fsqlmodel.get(engine, User, 1)
print(u)

# 删除
fsqlmodel.delete_id(engine, User, 1)

# 查询id为1的数据
u = fsqlmodel.get(engine, User, 1)
print(u)
```

## 版本历史

### v0.1.0

- 常见的增删改查功能

## 说明

如果你对Python感兴趣，需要一对一的指导，欢迎私信我，包教会。