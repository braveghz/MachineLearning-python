### io编程

#### 读写文件

```python
with open('/path/to/file', 'r') as f:
    print f.read()
```

- `read()`会一次性读取文件的全部内容
- `read(size)`每次最多读取size个字节的内容
- `readline()`可以每次读取一行内容
- `readlines()`一次读取所有内容并按行返回`list`

```python
for line in f.readlines():
    print(line.strip()) # 把末尾的'\n'删掉
 
with open('/Users/michael/test.txt', 'w') as f:
    f.write('Hello, world!')
```

#### 文件 ／ 目录

```python
import os
os.name # 操作系统的名字
# posix----系统是Linux、Unix、Mac OS X ；如果是nt，就是Windows系统
os.uname() # 获取详细的系统信息
os.environ # 环境变量
os.getenv('PATH') #获取某个环境变量的值
os.path.abspath('.') #获取绝对路径
os.mkdir('xxxx') #创建目录
os.emdir('xxxx') #删除目录
os.path.join('/Users/michael', 'testdir') #合并路径
	'/Users/michael/testdir'
os.path.split('/Users/michael/testdir/file.txt') #拆分路径
	('/Users/michael/testdir', 'file.txt')
os.rename('test.txt', 'test.py') # 文件重命名
os.remove('test.py') # 删掉文件
# 列出当前目录下的所有目录
[x for x in os.listdir('.') if os.path.isdir(x)]
['.lein', '.local', '.m2', '.npm', '.ssh', '.Trash', '.vim', 'Adlm', 'Applications', 'Desktop', ...]
# 列出所有的.py
[x for x in os.listdir('.') if os.path.isfile(x) && os.path.split(x)[1] == 'py']
```

#### 序列化

##### 序列化

序列化：把变量变成可存储or传输的过程 pickling，序列化之后可以将序列化后的内容写到磁盘or网络传输。反过来，把变量内容从序列化的对象重新读到内存中称为*反序列化*，unpickling。

```python
try:
    import cPickle as pickle #cPickle 是c写的，速度快
except ImportError:
    import pickle
    
d = dict(name='Bob', age=20, score=88)
## no1
pickle.dumps(d)
"(dp0\nS'age'\np1\nI20\nsS'score'\np2\nI88\nsS'name'\np3\nS'Bob'\np4\ns."

## no2
f = open('dump.txt', 'wb')
pickle.dump(d, f)
f.close()

## 读出序列化的内容
f = open('dump.txt', 'rb')
d = pickle.load(f)
f.close()
>>> d
{'age': 20, 'score': 88, 'name': 'Bob'}
```

只用Pickle保存那些不重要的数据，不能成功地反序列化也没关系。

##### JSON

```python
import json
d = dict(name='Bob', age=20, score=88)

# 序列化
>>> json.dumps(d) # 返回str
'{"age": 20, "score": 88, "name": "Bob"}'

# 反序列化
json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> json.loads(json_str)
{u'age': 20, u'score': 88, u'name': u'Bob'}
# 反序列化后的内容默认是 unicode
```

###### 将一个类的实例序列化／反序列化

```python
import json

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

s = Student('Bob', 20, 88)

# 序列化
# 先将student的实例转化为dict再序列化为json
def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }

print(json.dumps(s, default=student2dict))

# 偷懒写法
print(json.dumps(s, default=lambda obj: obj.__dict__))
# 通常类的实例的__dict__属性存储了实例变量
# 但是有例外，比如定义了__slots__ 的类

# 反序列化
def dict2student(d): #将dict转换为student实例
    return Student(d['name'], d['age'], d['score'])
json_str = '{"age": 20, "score": 88, "name": "Bob"}'
# loads()函数得到dict对象
print(json.loads(json_str, object_hook=dict2student))
```