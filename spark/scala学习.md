---
title: Spark的Scala学习
tags: 
- MachineLearning
- Spark
---
# Python的Spark学习

[Spark入门之Scala语言解释及实例](https://www.ibm.com/developerworks/cn/opensource/os-cn-spark-scala/index.html)

解释性语言，可以直接翻译执行
Scala 的所有变量都是对象
生成的结果res0，res1..也可以在后面直接用

可以编写 `.scala `文件
```s
[root@localhost:4 bin]# cat hello.scala
println("Hello, world, from a script!")
[root@localhost:4 bin]# ./scala hello.scala
Hello, world, from a script!
```

```s
class MyClass(index: Int, name: String)
#两个私有字段的类，一个名为 index 的 int 类型和一个叫做 name 的 String 类型，还有一个用这些变量作为参数获得初始值的构造函数。
```