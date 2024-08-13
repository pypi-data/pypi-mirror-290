pycodeobject����һ�����ڽ������༭�ʹ���Python�ֽ���(bytecode)�Ĺ��ߡ�

Pycodeobject is a tool for parsing and processing Python bytecode object.

��ϸ����
========

�ֽ���Ľṹ
"""""""""""""""""""""""

������֪, Python�е��ֽ���(bytecode) ��һ����������, Python����ı���������bytecode����

bytecode�����������������غ�ֱ�����У���pyc�ļ�����bytecode��Ӳ���ϵı�����ʽ��
��ͨ��һ��ʾ��, ����ʲô���ֽ���::

.. code-block:: python

    >>> import dis
    >>> def f(x):print('hello',x)
    
    >>> f.__code__
    <code object f at 0x02B27498, file "<pyshell#2>", line 1>
    >>> f.__code__.co_code
    b't\x00d\x01|\x00\x83\x02\x01\x00d\x00S\x00'
    >>> dis.dis(f)
      1           0 LOAD_GLOBAL              0 (print)
                  2 LOAD_CONST               1 ('hello')
                  4 LOAD_FAST                0 (x)
                  6 CALL_FUNCTION            2
                  8 POP_TOP
                 10 LOAD_CONST               0 (None)
                 12 RETURN_VALUE
    >>> 

����ʾ����f.__code__����bytecode����, f.__code__.co_code���Ƕ����Ƶ��ֽ���, ͨ��disģ����Է����롢������Щ�����ƴ��롣

Python����ִ�д���ʱ, �����Ƚ�ԭʼ��Դ���뷭���bytecode��ʽ, ��ֱ��ִ��bytecode, ��������ܡ�

.. image:: https://img-blog.csdnimg.cn/20210719105023666.png
    :alt: �ֽ���ṹͼ

(�� Python 3.8��, ������һ������ `co_posonlyargcount`)

�꾡��˵���μ�Python�ٷ��ĵ� https://docs.python.org/zh-cn/3.7/library/dis.html ��

��װ�ֽ���
""""""""""""""""""""

��python��, bytecode����������ǲ����޸ĵġ���::

.. code-block:: python

    >>> def f():pass
    >>> f.__code__.co_code = b''
    Traceback (most recent call last): ... ...
    AttributeError: readonly attribute

Ϊ��ʹbytecode���������, ����Ŀ�е�Code��, ���ڰ�װ (wrap)�ֽ������

�����ʾ���Ǵ�doctest��ժȡ��::

.. code-block:: python

    >>> def f():print("Hello")
    >>> c=Code.fromfunc(f)
    >>> c.co_consts
    (None, 'Hello')
    >>> c.co_consts=(None, 'Hello World!')
    >>> c.exec()
    Hello World!
    >>>
    >>> import os,pickle
    >>> temp=os.getenv('temp')
    >>> with open(os.path.join(temp,"temp.pkl"),'wb') as f:
    ...     pickle.dump(c,f)
    ... 
    >>> f=open(os.path.join(temp,"temp.pkl"),'rb')
    >>> pickle.load(f).to_func()()
    Hello World!
    >>> 
    >>> c.to_pycfile(os.path.join(temp,"temppyc.pyc"))
    >>> sys.path.append(temp)
    >>> import temppyc
    Hello World!
    >>> Code.from_pycfile(os.path.join(temp,"temppyc.pyc")).exec()
    Hello World!

�汾 VERSION
============
    1.0.4

	**��pyobject��Ĺ�ϵ**

	pycodeobject����������ߵ�����������Ŀ��������pyobject��Ŀ�����pycodeobject�ⱻ�ϲ�����pyobject.codeģ���С�

���� AUTHOR
===========
    qfcy qq:3076711200 �����˺�:qfcy\_

    ����CSDN��ҳ: https://blog.csdn.net/qfcy\_
