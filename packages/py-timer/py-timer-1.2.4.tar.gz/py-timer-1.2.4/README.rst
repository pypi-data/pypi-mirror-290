**����: ���ڱ�ģ�������timer��pywin32���е�timerģ�����Ƴ�ͻ����ģ�������ú�ֹͣ���£��밲װ�������°汾��timer-toolģ�飨https://pypi.org/project/timer-tool/����**

**Warning: Due to a naming conflict with the timer module in the pywin32 library, this module has been deprecated and will no longer be maintained. Please install the author's latest version of module timer-tool (https://pypi.org/project/timer-tool/).**

ģ������ MODULE NAME
====================

::

    timer

��� DESCRIPTION
================

::

    A Python timer module, containing class Timer() and decorator function timer(), 
    as well as some useful functions that can be used for performance analysis.
    һ��Python��ʱ��ģ��, ���а���Timer()���timer()װ����, �Լ�һЩ��ص����ú���, �����ڳ������ܷ�����

�����ĺ������� Functions & Classes:
===================================

��:

class Timer
"""""""""""
    һ����ʱ����
    
    start()
        ��ʼ��ʱ���˷�����Timer���ʼ��ʱ�ᱻ�Զ����á�
    
    gettime()
        ��ȡ�Ӽ�ʱ��ʼ�����ڵ�ʱ�䡣
    
    printtime(fmt_str="��ʱ:{:.8f}��")
        ��ӡ���Ӽ�ʱ��ʼ�����ڵ�ʱ��, Ҳ���ǻ�ȡ��ֵ��

����: 

timer(msg=None, file=sys.stdout, flush=False)::

    һ��װ����, Ϊĳ��������ʱ (��ʹ��Timer����졢����)��
    �÷�:@timer(msg="��ʱ:{time}��")
    def func(args):
        print("Hello World!")
    
    #��:
    @timer
    def func(args):
        print("Hello World!")

ʾ������ EXAMPLES
=================

ʾ��1:

.. code-block:: python

    import timer
    t=timer.Timer() #��ʼ��Timer����
    do_something()
    t.printtime() #���ִ��do_something()����ʱ�� (Ҳ��ʹ��t.gettime()��ȡ����ʱ��)

ʾ��2:

.. code-block:: python

    #�˳�with���ʱ�Զ���ӡ������ʱ�䡣
    import timer
    with timer.Timer(): #�����￪ʼ��ʱ
        do_something()

ʾ��3:

.. code-block:: python

    # Ϊĳ��������ʱ
    from timer import timer
    @timer
    def func():
        print("Hello World!")

ʾ��4:

.. code-block:: python

    # ����ȷ���ӳ�һ��ʱ��
    from time import sleep
    from timer import sleep as sleep2
    sleep(0.0001)
    sleep2(0.0001)
    # �����Ա���, timeģ���sleep()�����뱾ģ��ĺ������, �����Ե��ӳ�

�汾 VERSION
============

    1.2.4

    **����: ���ڱ�ģ�������timer��pywin32���е�timerģ�����Ƴ�ͻ����ģ�������ú�ֹͣ���£��밲װ�������°汾��timer-toolģ�飨https://pypi.org/project/timer-tool/����**

���� AUTHOR
===========

    �߷ֳ��� qq:3076711200

    ����CSDN��ҳ: https://blog.csdn.net/qfcy\_