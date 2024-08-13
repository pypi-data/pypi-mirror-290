ģ������ MODULE NAME
====================

::

    timer_tool

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
    һ����ʱ���ࡣA timer class.
    
    start()
        ��ʼ��ʱ���˷�����Timer���ʼ��ʱ�ᱻ�Զ����á�
		Start timing. This method will be automatically called when the Timer class is initialized.
    
    gettime()
        ��ȡ�Ӽ�ʱ��ʼ�����ڵ�ʱ�䡣
		Get the elapsed time since the timer started.
    
    printtime(fmt_str="��ʱ:{:.8f}��")
        ��ӡ���Ӽ�ʱ��ʼ�����ڵ�ʱ��, Ҳ����gettime()��ȡ��ֵ��
		Print the time elapsed since the timer started, which is the value obtained from gettime().

����: 

timer(msg=None, file=sys.stdout, flush=False)::

    һ��װ����, Ϊĳ����������������ʱ (��ʹ��Timer������)��
	A wrapper for timing a function or a generator that is briefer than the Timer class.
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

    import timer_tool
    t=timer.Timer() #��ʼ��Timer����
    do_something()
    t.printtime() #���ִ��do_something()����ʱ�� (Ҳ��ʹ��t.gettime()��ȡ����ʱ��)

ʾ��2:

.. code-block:: python

    #�˳�with���ʱ�Զ���ӡ������ʱ�䡣
    import timer_tool
    with timer.Timer(): #�����￪ʼ��ʱ
        do_something()

ʾ��3:

.. code-block:: python

    # Ϊĳ��������ʱ
    from timer_tool import timer
    @timer
    def func():
        print("Hello World!")

ʾ��4:

.. code-block:: python

    # ����ȷ���ӳ�һ��ʱ��
    from time import sleep
    from timer_tool import sleep as sleep2
    sleep(0.0001)
    sleep2(0.0001)
    # �����Ա���, timeģ���sleep()�����뱾ģ��ĺ������, �����Ե��ӳ�

�汾 VERSION
============

    1.2.4

���� AUTHOR
===========

    qfcy (�߷ֳ���) qq:3076711200

    ����CSDN��ҳ: https://blog.csdn.net/qfcy\_