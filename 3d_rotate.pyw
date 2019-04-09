__doc__ = '''简单三维树'''

from turtle import Turtle, Screen, done
from math import sin, cos, tan, pi
from random import randint

# ============ 1. 初始化部分 ============
t = Turtle('circle')
t.hideturtle()
t.penup()
# t.screen.delay(0)
t.color('white', 'black')
t.setundobuffer(2)

screen = Screen()
screen.bgcolor('black')
screen.tracer(0)

# ============ 2. 三维向量函数部分 ============


# 取输入向量方向的单位向量
def get_unit_vector(v):
    l = (v[0]**2 + v[1]**2 + v[2]**2)**0.5
    return [i / l for i in v]


# 根据输入向量获取一组正交基
# 由恒等式获取第一个垂直向量
# 再由两向量外积得到第三个向量
def get_base_vectors(v):
    a, b, c = tuple(v)
    v1 = [b - c, c - a, a - b]
    v2 = [
        a * b - b**2 - c**2 + a * c, a * b + b * c - a**2 - c**2,
        a * c - a**2 - b**2 + b * c
    ]
    return get_unit_vector(v1), get_unit_vector(v2)


# 返回向量v1、v2的和
def add(v1, v2):
    return [i + j for i, j in zip(v1, v2)]


# 返回向量v与数值a的乘积
def mul(v, a):
    return [i * a for i in v]


# ============ 3. 绘制树部分 ============

# 记录需画在最上层的节点
elements = []


# 递归生成函数
def tree(pos, direction, floor, length):
    '''
    根据三维的方向向量绘制伪3D树
    pos : 起始坐标（三维）
    direction : 前进方向（三维单位向量）
    floor : 剩余递归层数
    length : 树枝长度
    '''
    # 生成新树枝
    pos_new = add(pos, mul(direction, length))
    elements.append((0, pos, pos_new, floor))

    # 若剩余层数大于1则分枝
    if floor > 1:
        # 获取必要参数
        b1, b2 = get_base_vectors(direction)  # 正交基
        rexpand = randint(30, 45) * pi / 180  # 新方向与direction夹角
        rrotate = randint(1, 360) * pi / 180  # 在法平面旋转角度
        branches = randint(3, 5)  # 分枝个数
        for i in range(branches):
            # 计算在对应旋转角上的射影向量
            b = add(
                mul(b1, cos(rrotate + i * pi * 2 / branches)),
                mul(b2, sin(rrotate + i * pi * 2 / branches)))

            # 计算出新的单位向量方向并分枝
            newd = get_unit_vector(add(direction, mul(b, tan(rexpand))))
            tree(pos_new, newd, floor - 1, length - 10)

    # 否则绘制节点树叶
    else:
        elements.append((1, pos_new))


# 绘制函数
def draw(angle):
    depth = list(map(lambda x: x[1][0] * cos(angle) + x[1][2] * sin(angle),
                elements))
    try:
        max_depth=max(depth)
        min_depth=min(depth)
        d_map=lambda d:0.2+0.8*(d-min_depth)/(max_depth-min_depth)
    except:
        d_map=lambda d:1
    ordered = sorted(zip(elements, depth), key=lambda x: x[1])
    screen._delete("all")
    for e, depth in ordered:
        col=d_map(depth)
        t.color((col,)*3,(col/2,)*3)
        t.goto(e[1][0] * sin(angle) - e[1][2] * cos(angle), e[1][1])
        if e[0]:
            t.stamp()
        else:
            t.pensize(e[3])
            t.pd()
            t.goto(e[2][0] * sin(angle) - e[2][2] * cos(angle), e[2][1])
            t.pu()
    screen.update()


# ============ 4. 窗口控制部分 ============
ANGLE = 0
DRAGGING = False


def dragging(event):
    if not DRAGGING:
        return
    global ANGLE
    ANGLE = dragging.begin_angle + (event.x - dragging.begin_x) * 0.05
    draw(ANGLE)


def enterDrag(event):
    global DRAGGING
    dragging.begin_x = event.x
    dragging.begin_angle = ANGLE
    DRAGGING = True


def exitDrag(event):
    global DRAGGING
    DRAGGING = False


screen._root.bind("<B1-Motion>", dragging)
screen._root.bind("<Button-1>", enterDrag)
screen._root.bind("<ButtonRelease-1>", exitDrag)

# ============ 5. 运行 ============

# 生成树
tree((0, -350, 0), (0, 1, 0), 5, 150)

# 绘制内容
draw(ANGLE)

# 结束
done()