from collections import deque as dq
from threading import Thread, Lock
from time import sleep
from random import random as rnd

from PIL import ImageGrab
from os import mkdir
from os.path import join as join_path

from turtle import Turtle, Screen, done, tracer

import random


class TreeSplitter():
    '''
    用于将输入参数形如(turtle [, *args [, **kwargs]])的turtle递归函数多线程化
    实例化后为函数装饰器形式
    param turtle_gen : 生成turtle的函数
    max_turtle : 最大同时运行turtle数目
    stack_like : 线程池是否为LIFO，默认为否
    helper_func : 主循环线程的伴随函数
    '''

    ### 装饰器初始化
    def __init__(self,
                 turtle_gen,
                 max_turtle=1,
                 stack_like=False,
                 helper_func=None):
        '''
        初始化装饰器对象
        '''
        # 线程池
        self._sprouts = dq()
        self._sprout_stack = stack_like

        # 记录当前运行turtle
        self._running_turtles = 0
        self._turtle_count = max_turtle
        self._qlock = Lock()

        # 用于调用的turtle队列
        self._turtles = dq()
        for i in range(max_turtle):
            self._turtles.append(turtle_gen())

        # 记录主循环线程是否已在运行
        self._looping = False

        # 与主循环同时运行的伴随线程
        self._helper_func = helper_func

    ### turtle队列资源分配部分
    def _acquire_turtle(self):
        '''
        获取一个turtle，将工作计数加1
        '''
        with self._qlock:
            self._running_turtles += 1
            turtle_branch = self._turtles.pop()
        return turtle_branch

    def _return_turtle(self, turtle_branch):
        '''
        归还一个turtle至队列，将工作计数减1
        turtle_branch : 归还的turtle
        '''
        with self._qlock:
            self._turtles.append(turtle_branch)
            self._running_turtles -= 1

    ### 函数装饰部分
    def _wrapper_inner(self, func, *args, **kwargs):
        '''
        对原函数的内层包装
        用于由队列获取turtle并更新运行线程数目
        '''
        # 由队列获取一个turtle
        turtle_branch = self._acquire_turtle()

        # 以原参数运行被修饰函数
        func(turtle_branch, *args, **kwargs)

        # 归还turtle
        self._return_turtle(turtle_branch)

    def __call__(self, func):
        '''
        修饰器函数
        被调用时返回目标函数的修饰结果
        func : 原函数
        '''

        def wrapper_outer(dummy, *args, **kwargs):
            '''
            外层包装函数
            dummy : 不接收原始的turtle参数，使用内部分配的turtle
            *args, **kwargs : 其余参数
            '''
            # 向线程池中添加内层包装函数，参数为目标函数与原参数
            sprout = Thread(
                target=self._wrapper_inner, args=(func, *args), kwargs=kwargs)
            self._sprouts.append(sprout)

            # 启动循环线程，并添加至主进程
            if not self._looping:
                self._looping = True
                self._loopthr = Thread(target=self._mainloop)
                self._loopthr.setDaemon(True)
                self._loopthr.start()

                # 启动伴随线程
                if self._helper_func:
                    self._helper_thr = Thread(
                        target=self._helper_func, args=(self._loopthr, ))
                    self._helper_thr.setDaemon(True)
                    self._helper_thr.start()

        return wrapper_outer

    ### 循环线程部分
    def _mainloop(self):
        '''
        启动后循环检查线程池与运行线程，并以最大线程数运行
        线程池清空后隐藏所有turtle
        '''
        # 进入主循环
        print('%d parallel thread(s) loaded' % self._turtle_count)
        while self._running_turtles > 0 or len(self._sprouts) > 0:
            # 等待可用线程且当前线程数小于最大线程数
            if self._running_turtles >= self._turtle_count or len(
                    self._sprouts) == 0:
                sleep(0.005)
                continue

            # 线程池按照栈或者队列形式运行
            if self._sprout_stack == 'random':
                if rnd() < 0.5:
                    thr = self._sprouts.pop()
                else:
                    thr = self._sprouts.popleft()
            elif self._sprout_stack:
                thr = self._sprouts.pop()
            else:
                thr = self._sprouts.popleft()

            # 开始线程
            thr.start()

        # 隐藏所有turtle，展示结果
        print('Done.')
        for t in self._turtles:
            t.hideturtle()
        t.screen.update()


def turtleshot(timespan, folder_name, file_format, margin=10):
    '''
    返回一个循环截图turtle窗口的函数
    可用作TreeSplitter的伴随线程
    timespan : 截图时间间隔
    folder_name : 文件夹名称
    file_format : 截图jpg文件名称格式
    margin : 窗口边界
    '''

    def inner(mainloop):
        '''
        伴随函数
        mainloop : 接收主循环线程
        '''
        # 创建目录，生成文件名模板
        try:
            mkdir(folder_name)
        except:
            pass
        file_fm = join_path(folder_name, file_format)

        # 获取截图范围
        screen = Screen()
        canvas, root = screen.getcanvas(), screen._root

        # 截图
        print('screenshot begin.')
        index = 0
        while mainloop.is_alive():
            x = root.winfo_rootx() + canvas.winfo_x() + margin
            y = root.winfo_rooty() + canvas.winfo_y() + margin
            x1 = x + canvas.winfo_width() - margin
            y1 = y + canvas.winfo_height() - margin
            ImageGrab.grab().crop((x, y, x1, y1)).save(file_fm % index)
            sleep(timespan)
            index += 1
        ImageGrab.grab().crop((x, y, x1, y1)).save(file_fm % 9999)
        print('screenshot end.')

    return inner


def one_turtle_shot(file, margin=10):
    '''
    获取一张turtle界面截图
    file : jpg格式文件名
    margin : 窗口边界
    '''
    # 获取截图范围
    screen = Screen()
    canvas, root = screen.getcanvas(), screen._root

    # 截图
    x = root.winfo_rootx() + canvas.winfo_x() + margin
    y = root.winfo_rooty() + canvas.winfo_y() + margin
    x1 = x + canvas.winfo_width() - margin
    y1 = y + canvas.winfo_height() - margin
    ImageGrab.grab().crop((x, y, x1, y1)).save(file)


__all__ = ['TreeSplitter', 'turtleshot', 'one_turtle_shot']

if __name__ == '__main__':

    cell = int(input())

    if cell == 1:
        print('======= 1. TreeSplitter =======')

        def new_turtle():
            turtle_branch = Turtle()
            turtle_branch.penup()
            turtle_branch.hideturtle()
            turtle_branch.speed(0)
            turtle_branch.screen.delay(0)
            turtle_branch.pencolor('brown')
            turtle_branch.fillcolor('green')
            turtle_branch.shape('circle')
            return turtle_branch

        @TreeSplitter(new_turtle, 1, True)
        def tree(tt, pos, size, angle, floor):
            def leaf(color, size):
                tt.pencolor(color)
                tt.fillcolor(color)
                tt.shapesize(size)
                tt.stamp()

            tt.goto(pos)
            tt.setheading(angle)
            tt.pensize(size / 8)
            tt.pencolor(
                random.randint(40, 60) * 0.01,
                random.randint(20, 30) * 0.01,
                random.randint(10, 20) * 0.01)
            tt.pendown()
            size *= random.randint(70, 120) * 0.01
            tt.forward(size)  #前进画树
            tt.penup()  #返回不画树
            if floor > 0:
                pp = tt.pos()
                for i in range(1, 4):
                    tree(tt, pp, size - 10,
                         angle + random.randint(-15 * i, 15 * i), floor - 1)
                if random.randint(0, 30) < 10:
                    leaf((random.randint(10, 30) * 0.01,
                          random.randint(60, 80) * 0.01,
                          random.randint(20, 40) * 0.01),
                         random.randint(10, 20) * 0.1)
            else:
                leaf((random.randint(10, 30) * 0.01,
                      random.randint(60, 80) * 0.01,
                      random.randint(20, 40) * 0.01),
                     random.randint(40, 50) * 0.1)
            tt.setheading(angle + 180)
            tt.forward(size)

        tree(new_turtle(), (0, -350), 135, 90, 5)
        done()

    if cell == 2:
        print('======= 2. Double Tree =======')
        screen = Screen()
        screen.bgcolor('black')

        def newturtle():
            t = Turtle()
            t.color('white')
            t.penup()
            t.screen.delay(0)
            t.speed(0)
            return t

        @TreeSplitter(newturtle, 10)
        def tree(tt, pos, angle, floor, length):
            tt.goto(pos)
            tt.setheading(angle)
            tt.pendown()
            tt.forward(length)
            tt.penup()

            if floor > 0:
                cpos = tt.pos()
                tree(tt, cpos, angle - 16, floor - 1, length / 1.2)
                tree(tt, cpos, angle + 16, floor - 1, length / 1.2)
            else:
                tt.stamp()

        tracer(10)
        tree(None, (400, -400), 120, 10, 150)
        tree(None, (-400, -400), 60, 10, 150)

        done()

    if cell == 3:
        print('======= 3. Maze =======')
        screen = Screen()
        screen.bgcolor('black')

        def new_turtle():
            tt = Turtle('circle')
            tt.color('white')
            tt.penup()
            tt.speed(0)
            return tt

        gen_map = set()
        gap = 15
        goto = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        @TreeSplitter(new_turtle, 1, 'random')
        def rand_gen(tt, x, y, dx, dy, floor, max_floor=40, color='white'):
            tt.color(color)
            tt.goto(x * gap, y * gap)
            if dx:
                tt.setheading(90 - 90 * dx)
            else:
                tt.setheading(90 * dy)
            if floor == 0:
                gen_map.add((x, y))
            target = (x + dx, y + dy)
            if target in gen_map:
                return
            gen_map.add(target)
            tt.pensize((max_floor - floor) / max_floor * gap)
            tt.pendown()
            tt.goto((x + dx) * gap, (y + dy) * gap)
            tt.penup()

            if floor < 40:
                random.shuffle(goto)
                for d in goto:
                    if d != (-dx, -dy):
                        rand_gen(tt, *target, *d, floor + 1, max_floor, color)
            else:
                tt.stamp()

        tracer(100)
        rand_gen(None, 15, 0, 1, 0, 0, 40, 'green')
        rand_gen(None, -9, -12, -1, 0, 0, 40, 'blue')
        rand_gen(None, -9, 12, -1, 0, 0, 40, 'red')
        rand_gen(None, 0, 0, 1, 0, 0, 40)

        done()