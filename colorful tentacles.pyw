# ============ 可修改参数 ============
鼠标控制范围=200# 正数，为按住鼠标作用范围
加强系数=0# 受按住鼠标作用时枝条变粗速度
变色系数=1# 受按住鼠标作用时变色程度
衰减系数=0.97# 小数，大于0小于1

速度系数=1# 调节枝条前进速度，大于0
卷曲系数=1# 调节枝条弯曲程度

帧频=30# 每秒（最大）更新次数



from turtle import Turtle, Vec2D, Screen, tracer, update, done
from colorsys import hls_to_rgb
from random import randint
from time import perf_counter as pf,sleep

# ============ 1. 全局初始化 ============
MAX_BRANCHES = 15  # 最大活动turtle数
BORDERX, BORDERY = 400, 400  # 画框大小
tracer(0)  # 禁止自动更新

screen = Screen()
DRAGGING = False

# 初始化所有乌龟
TURTLES = [Turtle('turtle') for i in range(MAX_BRANCHES)]
for t in TURTLES:
    t.penup()
    t.speed(0)
    t.screen.delay(0)
    t.hideturtle()

# 绘制画框
tcursor = Turtle('circle')
tcursor.penup()
tcursor.goto(-BORDERX, -BORDERY)
tcursor.pendown()
tcursor.setx(BORDERX)
tcursor.sety(BORDERY)
tcursor.setx(-BORDERX)
tcursor.sety(-BORDERY)
tcursor.penup()


# ============ 2. 类定义 ============
class Branch:
    pool = []

    def __init__(self, pos, angle, size, hue):
        if not TURTLES:
            return

        self.size = size
        self.hue = hue
        self.dr = randint(-100, 100) / 50

        self.pen = TURTLES.pop()
        self.pen.penup()
        self.pen.goto(pos)
        self.pen.setheading(angle)
        self.pen.pensize(size*2)
        self.set_color()
        self.pen.pendown()
        Branch.pool.append(self)

    def set_color(self):
        clr = hls_to_rgb((self.hue % 200) / 200, 0.5 - self.size * 0.02, 1)
        self.pen.color(clr)

    def clone(self):
        b = Branch(self.pen._position, self.pen.heading(), self.size, self.hue)
        b.dr = randint(-300, 300) / 50

    def update(self):
        if self.size < 1 or abs(self.pen._position[0]) > BORDERX or abs(
                self.pen._position[1]) > BORDERY:
            return self.terminate()
        self.pen.pensize(self.size*2)
        self.set_color()
        self.pen.forward(self.size*速度系数)
        self.pen.left(self.dr*卷曲系数)
        if (self.size >= 3
                and randint(1, 15) == 1) or (3 > self.size >= 2
                                             and randint(1, 50) == 1):
            self.clone()
        if DRAGGING and abs(self.pen._position - tcursor._position) < 鼠标控制范围:
            self.size += 加强系数
            self.hue += 变色系数
        else:
            self.size *= 衰减系数

    def terminate(self):
        self.pen.penup()
        TURTLES.append(self.pen)
        Branch.pool.remove(self)

    @staticmethod
    def update_branches():
        for b in Branch.pool[:]:
            b.update()


# ============ 3. 控制函数定义 ============


def dragging(event):
    tcursor.goto(event.x - screen._root.winfo_width() / 2,
                 -event.y + screen._root.winfo_height() / 2)


def enterDrag(event):
    tcursor.showturtle()
    global DRAGGING
    DRAGGING = True
    dragging(event)


def exitDrag(event):
    tcursor.hideturtle()
    global DRAGGING
    DRAGGING = False


# ============ 4. 主逻辑 ============
screen._root.bind("<B1-Motion>", dragging)
screen._root.bind("<Button-1>", enterDrag)
screen._root.bind("<ButtonRelease-1>", exitDrag)
Branch.pool.append(Branch((0, -300), 90, 20, randint(1, 200)))

timer=pf()
while 1:
    now=pf()
    if now-timer<1/帧频:
        sleep(timer+1/帧频-now)
    timer=pf()
    Branch.update_branches()
    update()
