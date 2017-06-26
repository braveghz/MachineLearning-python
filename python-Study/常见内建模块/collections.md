### collections

#### namedtuple

```python
from collections import namedtuple
# namedtuple('名称', [属性list])
Point = namedtuple('Point',['x','y'])
p = Point(1,2)
>>> p.x
1
```

#### deque

高效实现插入和删除操作的双向列表，适合用于队列和栈

支持`append()` ／ `pop() `／ `appendleft() `／ `popleft()`

```python
from collections import deque
q = deque(['a','b','c'])
q.append('x')
q.appendleft('y')
>>> q
deque(['y','a','b','c','x'])
```

#### defaultdict

dict的key不存在时抛出 `KeyError`

用`defaultdict`使得key不存在时返回默认值

```python
from collections import defaultdict
dd = defaultkey(lambda:'N/A')
dd['k1'] = 'k1'
>>> dd['k1']
k1
>>> dd['k2'] #k2不存在，返回默认值
'N/A'
```

#### OrderedDict

key有顺序的dict

```python
from collections import OrderedDict
d = dict([('a',1),('b',2),('c',3)])
>>> d #dict的Key是无序的
{'a': 1, 'c': 3, 'b': 2}
od = OrderedDict([('a',1),('b',2),('c',3)])
>>> od # 按照key插入的顺序
OrderedDict([('a',1),('b',2),('c',3)]) 
```

------

实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key：

```python
from collections import OrderedDict

class LastUpdatedOrderedDict(OrderedDict):

    def __init__(self, capacity):
        super(LastUpdatedOrderedDict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last=False)
            print 'remove:', last
        if containsKey:
            del self[key]
            print 'set:', (key, value)
        else:
            print 'add:', (key, value)
        OrderedDict.__setitem__(self, key, value)
```

#### Counter

计数器，ex统计字符出现的次数

```python
from collections import Counter
c = Counter()
for ch in 'programming':
    c(ch)=c(ch)+1
>>> c
Counter({'g': 2, 'm': 2, 'r': 2, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'p': 1})
```