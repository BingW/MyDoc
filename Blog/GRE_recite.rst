===========
Geek 背单词 
===========


Info
~~~~

+---------------+-----------------------------------------------------+
| Project Term: | Geek 背单词                                         |
+===============+=====================================================+
| Description:  | A little script to help recite GRE words            |
+---------------+-----------------------------------------------------+
| Author:       | BingWang                                            |
+---------------+-----------------------------------------------------+
| Last Modify:  | |today|                                             | 
+---------------+-----------------------------------------------------+
| Version:      | 0.10                                                |
+---------------+-----------------------------------------------------+

Introduction
~~~~~~~~~~~~
    
    简单的介绍一下，以后有机会再翻译成英文。
    
character
---------
    
艾宾浩斯曲线
    这个程序使用了艾宾浩斯曲线作为复习策略。每次程序启动时会根据每个单词的距离上次背诵的时间t，记忆强度s和难度d计算记忆率R，每次只复习那些需要复习的单词，即R < R_threshold。

.. math::
    
    R = e^{-\cfrac{t\cdot d}{s}}
    
Group
    用 `Smith-Waterman 算法 <http://en.wikipedia.org/wiki/Smith-Waterman_algorithm>`_ 对GRE单词进行Group，即相似的单词会被分到一个组，按组来背单词。
    
实时回馈
    命令(P)显示本次学习的时间，复习了多少单词，复习的速度，背了多少新词，背新词的速度，一共进行了百分之多少的进度。

自动保存
    每次退出程序(Q)时自动保存，此外每分钟（以背单词的时间计算而非程序运行时间）会自动保存一次。

TODO character
--------------

+ 增加浏览模式
+ 增加记忆率计算
+ 改进difficulty计算
    #. 利用每个单词花的时间给difficulty分级
+ 增加timeout功能

Interface
---------

Start:
    .. image:: images/GRE_interface1.png

Help:
    .. image:: images/GRE_interface2.png

Status:
    .. image:: images/GRE_interface3.png
    
Source Code
-----------

.. literalinclude:: codes/words.py
    :language: python
    :encoding: utf-8

