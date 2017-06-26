### base64编码

64个字符表示任意二进制数据

一个包含64个字符的数组：

```python
['A', 'B', 'C', ... 'a', 'b', 'c', ... '0', '1', ... '+', '/']
```

emmm 然后将二进制数据，3个字节一大组共24bit，再分为4小组每小组6bit，得到4个数字作为索引查表得到对应的4个字符，就是编码后的字符串。

这样3字节——4字节，长度增加33%，好处是编码后的文本数据可以在邮件正文、网页等直接显示

最后不足3个字节的：用`\x00`字节在末尾补足，再在末尾加上1个或2个`=`号，表示补了多少字节，解码时自动忽略

```python
import base64
>>> base64.b64encode('i\xb7\x1d\xfb\xef\xff')
'abcd++//'
# 标准Base64编码后可能出现+和/，在URL中就不能直接作为参数
# 字符+和/分别变成-和_
>>> base64.urlsafe_b64encode('i\xb7\x1d\xfb\xef\xff')
'abcd--__'
>>> base64.urlsafe_b64decode('abcd--__')
'i\xb7\x1d\xfb\xef\xff'
```

= 也可能出现在base64编码中，但是 = 在url ／ cookie中有歧义，所以base64编码后将 = 去掉

```python
# 标准Base64:
'abcd' -> 'YWJjZA=='
# 自动去掉=:
'abcd' -> 'YWJjZA'
>>> safe_b64decode('YWJjZA')
'abcd'
```

解码的时候，加上`=`把Base64字符串的长度变为4的倍数

