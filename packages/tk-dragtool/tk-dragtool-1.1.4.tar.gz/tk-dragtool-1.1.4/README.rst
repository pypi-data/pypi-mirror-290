NAME
    tk_dragtool

DESCRIPTION ���
    �ṩ������϶�������tkinter�ؼ����ߵ�ģ�顣
    A module providing tools to drag and resize
    tkinter window and widgets with the mouse.

FUNCTIONS ����
    bind_drag(tkwidget, dragger)
        ����ҷ�¼���
        tkwidget: ���϶��Ŀؼ��򴰿�,
        dragger: ��������¼��Ŀؼ�,
        ����bind_drag��,������϶�draggerʱ, tkwidget�ᱻ�����϶�, ��dragger
        ��Ϊ��������¼��Ŀؼ�, λ�ò���ı䡣
        x �� y: ����ͬ�ϡ�

    bind_resize(tkwidget, dragger, anchor, min_w=0, min_h=0, move_dragger=True)
        �������¼���
        anchor: ���ŵķ�λ, ȡֵΪN,S,W,E,NW,NE,SW,SE,�ֱ��ʾ���������ϡ�����
        min_w,min_h: �÷���tkwidget���ŵ���С���(��߶�)��
        move_dragger: ����ʱ�Ƿ��ƶ�dragger��
        ����˵��ͬbind_drag������

    draggable(tkwidget)
        ����draggable(tkwidget) ʹtkwidget���϶���
        tkwidget: һ���ؼ�(Widget)��һ������(Wm)��
        x �� y: ֻ����ı�x�����y���ꡣ

    getpos()
        ��ȡ��굱ǰλ�á�

    move(widget, x=None, y=None, width=None, height=None)
        �ƶ��ؼ��򴰿�widget, �����Կ�ѡ��

EXAMPLES ʾ��

.. code-block:: python

    import tkinter as tk
    from tk_dragtool import draggable
    
    root=tk.Tk()
    btn=tk.Button(root,text="Drag")
    draggable(btn)
    btn.place(x=0,y=0)
    root.mainloop()

����Ч��:

.. image:: https://img-blog.csdnimg.cn/47f8708a1eef42d591e922b8b0eb12d7.png
    :alt: Ч��ͼ

�����ӵ�ʾ��, ʵ����8�������ֱ��Ĺ���:

.. code-block:: python

    btns=[] # ��btns�б�洢�����İ�ť
    def add_button(func,anchor):
        # func�������Ǽ��㰴ť������
        b=ttk.Button(root)
        b._func=func
        bind_resize(btn,b,anchor)
        x,y=func()
        b.place(x=x,y=y,width=size,height=size)
        b.bind('<B1-Motion>',adjust_button,add='+')
		b.bind('<B1-ButtonRelease>',adjust_button,add='+')
        btns.append(b)
    def adjust_button(event=None):
        # �ı��С���϶���,�����ֱ�λ��
        for b in btns:
            x,y=b._func()
            b.place(x=x,y=y)
    root=tk.Tk()
    root.title("Test")
    root.geometry('500x350')
    btn=ttk.Button(root,text="Button")
    draggable(btn)
    btn.bind('<B1-Motion>',adjust_button,add='+')
	btn.bind('<B1-ButtonRelease>',adjust_button,add='+')
    x1=20;y1=20;x2=220;y2=170;size=10
    btn.place(x=x1,y=y1,width=x2-x1,height=y2-y1)
    root.update()
    # ���������ֱ�, �����ǿؼ����ŵ��㷨
    add_button(lambda:(btn.winfo_x()-size, btn.winfo_y()-size),
               'nw')
    add_button(lambda:(btn.winfo_x()+btn.winfo_width()//2,
                       btn.winfo_y()-size), 'n')
    add_button(lambda:(btn.winfo_x()+btn.winfo_width(), btn.winfo_y()-size),
               'ne')
    add_button(lambda:(btn.winfo_x()+btn.winfo_width(),
                       btn.winfo_y()+btn.winfo_height()//2),'e')
    add_button(lambda:(btn.winfo_x()+btn.winfo_width(),
                       btn.winfo_y()+btn.winfo_height()), 'se')
    add_button(lambda:(btn.winfo_x()+btn.winfo_width()//2,
                       btn.winfo_y()+btn.winfo_height()),'s')
    add_button(lambda:(btn.winfo_x()-size, btn.winfo_y()+btn.winfo_height()),
               'sw')
    add_button(lambda:(btn.winfo_x()-size,
                    btn.winfo_y()+btn.winfo_height()//2), 'w')
    root.mainloop()

Ч��ͼ:

.. image:: https://img-blog.csdnimg.cn/a64c54ff7c7148d7b943ff194dbc5292.gif
    :alt: ������ʾ����Ч��ͼ

�汾:1.1.4 (����: �޸��˶�Linux��ϵͳ��֧������)

����:``�߷ֳ��� qq:3076711200``

����CSDN��ҳ: https://blog.csdn.net/qfcy\_/