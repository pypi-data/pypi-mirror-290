## 支持情况测试

测试平台： Ubuntu 20.04.3 LTS AMD64 (WSL 1)
用于进行测试的 Python 版本详细信息：

```plaintext
Python 3.9.19 (main, Mar 20 2024, 18:08:17) [GCC 9.4.0] on linux
```

运行重现项目自身测试的结果与 Python 3.8 下的测试结果完全相同，包括警告信息。

## 手工测试命令行选项功能

由于 `--语法树` 参数的差异已经在下文说明，且除了 `--反汇编` 选项以外，其他选项的行为在 Py3.9 和 Py3.8 版本间无明显差异，故仅列出 `--反汇编` 选项的输出结果。

### 反汇编字节码测试

使用`py3.8支持.md`文件中给出的`反汇编测试.ul`运行`木兰 --反汇编 反汇编测试.ul`，结果如下：

```plaintext
  1           0 LOAD_CONST               0 (0)
              2 STORE_NAME               0 (i)

  3     >>    4 LOAD_NAME                0 (i)
              6 LOAD_CONST               1 (10)
              8 COMPARE_OP               1 (<=)
             10 POP_JUMP_IF_FALSE       80

  4          12 LOAD_NAME                0 (i)
             14 LOAD_CONST               2 (1)
             16 INPLACE_ADD
             18 STORE_NAME               0 (i)

  6          20 SETUP_FINALLY           18 (to 40)

  7          22 LOAD_NAME                1 (__rem__)
             24 LOAD_NAME                0 (i)
             26 LOAD_CONST               3 (2)
             28 CALL_FUNCTION            2
             30 POP_JUMP_IF_FALSE       36

  8          32 POP_BLOCK
             34 JUMP_ABSOLUTE            4
        >>   36 POP_BLOCK
             38 JUMP_FORWARD            30 (to 70)

 10     >>   40 POP_TOP
             42 STORE_NAME               2 (Exception)
             44 POP_TOP
             46 SETUP_FINALLY           12 (to 60)
             48 POP_BLOCK
             50 POP_EXCEPT
             52 LOAD_CONST               4 (None)
             54 STORE_NAME               2 (Exception)
             56 DELETE_NAME              2 (Exception)
             58 JUMP_FORWARD            10 (to 70)
        >>   60 LOAD_CONST               4 (None)
             62 STORE_NAME               2 (Exception)
             64 DELETE_NAME              2 (Exception)
             66 RERAISE
             68 RERAISE

 12     >>   70 LOAD_NAME                3 (println)
             72 LOAD_NAME                0 (i)
             74 CALL_FUNCTION            1
             76 POP_TOP
             78 JUMP_ABSOLUTE            4
        >>   80 LOAD_CONST               4 (None)
             82 RETURN_VALUE
```

其中新出现了`RERAISE`操作码，关于其具体的作用以及其它差别，可以参考 [dis --- Python 字节码反汇编器 — Python 3.9.18 文档](https://docs.python.org/zh-cn/3.9/library/dis.html#opcode-RERAISE)。

### 语法树节点差异

Python 3.9 中，函数调用时的[关键字参数](https://docs.python.org/zh-cn/3.9/glossary.html#term-argument)必须提供`lineno`与`col_offset`属性，否则会出现形如如下的异常：`类型错误：required field "lineno" missing from keyword`。

----

(py39) (base) xuanwu@XuantekiMBP 刷题 % time 木兰 实用/数学/二十四点.ul
^CTraceback (most recent call last):
  File "/Users/xuanwu/opt/anaconda3/lib/python3.8/site-packages/木兰/环境.py", line 167, in 自定义导入
    return 加载木兰模块(名称, 全局, 源自, 目录相对层次)
  File "/Users/xuanwu/opt/anaconda3/lib/python3.8/site-packages/木兰/环境.py", line 59, in 加载木兰模块
    可执行码 = 分析并编译(木兰源码路径)
  File "/Users/xuanwu/opt/anaconda3/lib/python3.8/site-packages/木兰/环境.py", line 49, in 分析并编译
    with open(源码文件名, 'r', encoding='utf-8') as 文件:
FileNotFoundError: [Errno 2] No such file or directory: 'numexpr.ul'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/xuanwu/opt/anaconda3/lib/python3.8/site-packages/numpy/__init__.py", line 327, in <module>
    __mkl_version__ = "{MajorVersion}.{MinorVersion}.{UpdateVersion}".format(**mkl.get_version())
KeyboardInterrupt
 😰 ImportError：numpy.core.multiarray failed to import
“/Users/xuanwu/opt/anaconda3/lib/python3.8/site-packages/numexpr/__init__.py”第26行：from numexpr.interpreter import MAX_THREADS, use_vml, __BLOCK_SIZE1__
调用层级如下
见第1行：using numexpr
木兰 实用/数学/二十四点.ul  1.03s user 0.06s system 5% cpu 18.319 total