## Python-Basics

`r' ' `表示' '内部字符默认不转义

`'''…'''`表示多行字符串

`None`表示空值

字母数字互换

```python
>>> ord('A')
65
>>> chr(65)
'A'
```

以Unicode表示的字符串用`u'...'`表示，比如：

```python
>>> print u'中文'
中文
```

#### list

list是一种可变有序表,`len()`获得元素个数,使用索引表示元素，索引从0开始。

索引 -1 -2 -3 表示倒数第1个／2个.... 

> `classmates.append('Adam')` 末尾追加元素
>
> `classmates.insert(1, 'Jack'）`   插入指定位置
>
> `classmates.pop()`   删除末尾元素
>
> `classmates.pop(1)`    删除指定位置元素

`L = ['Apple', 123, True]` 元素数据类型可以不同

#### tuple

有序表元组tuple,一旦初始化就不能修改 `t = (1, 2)`,但是tuple里的list的元素可以变动

---

`range(5)`  生成的序列是从0开始小于5的整数

`raw_input() `读取用户输入内容 —— 以字符串的形式返回

> 字典`d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}`
>
> `pop(key)` — — 删除key及对应的value

> 集合 `s = set([1, 2, 3])`  输入的list可以重复，自动过滤
>
> `add(key)`
>
> `remove(key)`
>
> `s1 & s2`
>
> `s1 | s2`

#### 函数

 `abs()`   绝对值

`cmp(x, y) `   如果`x<y`，返回`-1`    ——  如果`x==y`，返回`0`  —— 如果`x>y`，返回`1`

内置数据类型转换

#### 切片

`L[0:3]`   / `L[:3]`  表示 索引0 / 1 / 2 

```python
L[1:3]
L[-2:]
L[-2:-1]
```

#### 迭代

`for k, v in d.iteritems()`    dict 同时迭代key和value

#### 列表生成式

```python
[x * x for x in range(1, 11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

[m + n for m in 'ABC' for n in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
```

> `isinstance(object, classinfo)   `       object是变量,classinfo 是类型
>
> 判断实例是否是这个类或者是否是这个类型      

----

#### map 

```python
map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9]) # 第一个参数为函数，第二个参数为要适用的list，返回一个list
['1', '2', '3', '4', '5', '6', '7', '8', '9']
```

#### reduce

reduce 将函数作用在序列[x1, x2, x3…]，第一个参数为函数，第二个参数为要适用的list

reduce把结果继续和序列的下一个元素做累积计算

```python
reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
```

####  filter

`filter()`	参数 ： 一个函数和一个序列

把传入的函数依次作用于每个元素，根据返回值是`True` or `False`决定保留or丢弃

---

#### 函数作为返回值

```python
def lazy_sum(*args):
    def sum():
        ....
    return sum
```

调用`lazy_sum`返回求和函数sum并保存了相关参数和局部变量，ex `f = lazy_sum(1, 3, 5, 7, 9)`，再调用f才会计算求和结果。

`lazy_sum()`每次调用都会返回一个新的函数，即使传入相同的参数

注意不要用循环的局部变量，返回的函数不会立即执行，最后都会变成最后一次赋值的变量

####  匿名函数

匿名函数`lambda x: x * x`

```
def f(x):
    return x * x
```

关键字`lambda`表示匿名函数，冒号前面的`x`表示函数参数

匿名函数只能有一个表达式，返回值即为表达式的结果

#### 装饰器 Decorator

代码运行期间动态增加功能   

```python
f.__name__   # 得到函数名字
```
举例

```python
def hello(fn):
    def wrapper():
        print "hello, %s" % fn.__name__
        fn()
        print "goodby, %s" % fn.__name__
    return wrapper

@hello
def foo():
    print "i am foo"
 
foo()
```

输出

```python
->$ python hello.py
hello, foo
i am foo
goodby, foo
```

#### 偏函数

```python
>>> int('12345')
12345
>>> int('12345', base=8)
5349
```

简单来说，`functools.partial`作用是，把一个函数的某些参数给固定住，也就是设置默认值，返回一个新的函数，调用这个新函数会更简单。

```python
import functools
int2 = functools.partial(int, base=2)
### 等同
def int2(x, base=2):
    return int(x, base)
```

#### 模块

一个`abc.py`的文件就是一个名字叫`abc`的模块

包，一个文件夹，下面有很多py文件（也就是说有很多模块），必须有`__init__.py` 来说明这是一个包

标准模板223333:

```python
#!/usr/bin/env python   ## 在Unix/Linux/Mac上运行
# -*- coding: utf-8 -*-    ## 使用标准UTF-8编码
' a test module '  ## 任何模块代码的第一个字符串都被视为模块的文档注释
__author__ = 'Michael Liao'  ## 作者
```

`__future__`   2/3语法兼容问题
