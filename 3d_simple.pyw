__doc__ = '''简单三维树'''

from turtle import Turtle, Screen, done
from math import sin, cos, tan
from random import randint

# ============ 1. 初始化部分 ============
t = Turtle('circle')
t.penup()
t.screen.delay(0)
t.color('white', 'black')

screen = Screen()
screen.bgcolor('black')

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
nodes = []


# 递归绘制函数
def tree(pos, direction, floor, length):
    '''
    根据三维的方向向量绘制伪3D树
    pos : 起始坐标
    direction : 前进方向（三维单位向量）
    floor : 剩余递归层数
    length : 树枝长度
    '''
    # 初始化位置、粗细
    t.goto(pos)
    t.pensize(floor)

    # 在direction方向上绘制树枝
    t.pd()
    t.goto(pos[0] + direction[0] * length, pos[1] + direction[1] * length)
    t.pu()

    # 若剩余层数大于1则分枝
    if floor > 1:
        # 获取必要参数
        b1, b2 = get_base_vectors(direction)  # 正交基
        p = t.pos()  # 当前位置
        rexpand = randint(30, 45) * 3.14159 / 180  # 新方向与direction夹角
        rrotate = randint(1, 360) * 3.14159 / 180  # 在法平面旋转角度
        branches = randint(3, 5)  # 分枝个数
        for i in range(branches):
            # 计算在对应旋转角上的射影向量
            b = add(
                mul(b1, cos(rrotate + i * 3.14159 * 2 / branches)),
                mul(b2, sin(rrotate + i * 3.14159 * 2 / branches)))

            # 计算出新的单位向量方向并分枝
            newd = get_unit_vector(add(direction, mul(b, tan(rexpand))))
            tree(p, newd, floor - 1, length - 15)

    # 否则绘制节点树叶
    else:
        # 一半概率直接绘制，另一半储存绘制于顶层
        if randint(1, 2) == 1:
            nodes.append(t._position)
        else:
            t.stamp()


# 绘制树
tree((0, -350), (0, 1, 0), 5, 150)

# 绘制剩余节点
for i in nodes:
    t.goto(i)
    t.stamp()

# 结束
done()