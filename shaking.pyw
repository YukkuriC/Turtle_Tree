__doc__ = '''递归绘制树
鼠标拖动控制转动方向'''

from turtle import *
from random import randint, random, randrange
from colorsys import hsv_to_rgb
from os import mkdir

# 初始化
tracer(0)
hideturtle()
setundobuffer(None)
pu()
FORCE = 300
dFORCE = 0
DRAGGING = False
y0 = -400
elements = []

# 光标
cursor = Turtle()
cursor.pu()
cursor.setheading(135)
cursor.shapesize(4)
cursor.fillcolor('white')
cursor.hideturtle()


# 画树
def gen_tree(pos, angle, l):
    goto(pos)
    setheading(angle)
    forward(l)
    new_pos = position()
    elements.append(element('line', (pos, new_pos), 'brown', size=l / 7))
    if l > 40:
        gen_tree(new_pos, angle, l * 0.8)
        gen_tree(new_pos, angle - 60, l * 0.4)
        gen_tree(new_pos, angle + 60, l * 0.4)
    else:
        elements.append(
            element(
                'point',
                new_pos,
                'green',
                'green',
                randint(100, 200) / 100,
                shape='turtle',
                angle=randint(1, 3600) / 10))


# 绘图元素
class element:
    def __init__(self, etype, pt, color=None, fill=None, size=1, **kwargs):
        self.type = etype
        self.pt = pt
        self.color = color
        self.fill = fill
        self.size = size
        self.shape = shape
        for key in kwargs:
            self.__setattr__(key, kwargs[key])


def transform(x, y):
    x1 = x + FORCE * (y - y0)**2 * 1e-6
    y1 = y - FORCE * (x1 * 5e-4)
    return x1, y1


def draw():
    clear()
    for e in elements:
        if e.type == 'point':
            shapesize(e.size)
            goto(transform(*e.pt))
            shape(e.shape)
            setheading(e.angle)
            if e.color:
                pencolor(e.color)
            if e.fill:
                fillcolor(e.fill)
            stamp()
        else:
            pensize(e.size)
            if e.type == 'line':
                pencolor(e.color)
                goto(transform(*e.pt[0]))
                pd()
                goto(transform(*e.pt[1]))
                pu()
            elif e.type == 'polygon':
                goto(transform(*e.pt[-1]))
                if e.color:
                    pencolor(e.color)
                    pd()
                if e.fill:
                    fillcolor(e.fill)
                    begin_fill()
                for i in e.pt:
                    goto(transform(*i))
                pu()
                end_fill()
            elif e.type == 'trace':
                goto(transform(*e.pt[0]))
                if e.color:
                    pencolor(e.color)
                    pd()
                if e.fill:
                    fillcolor(e.fill)
                    begin_fill()
                for i in e.pt[1:]:
                    goto(transform(*i))
                pu()
                end_fill()

    update()


def dragForce(event):
    global FORCE
    FORCE = (event.x - dragForce.tk.winfo_width() / 2) * 1.5
    cursor.goto(event.x - dragForce.tk.winfo_width() / 2,
                -event.y + dragForce.tk.winfo_height() / 2)
    # cursor._update()


def enterDrag(event):
    cursor.showturtle()
    global DRAGGING, dFORCE
    DRAGGING = True
    dFORCE = 0
    dragForce(event)


def exitDrag(event):
    cursor.hideturtle()
    global DRAGGING
    DRAGGING = False


screen = Screen()
dragForce.tk = screen._root
screen._root.bind("<B1-Motion>", dragForce)
screen._root.bind("<Button-1>", enterDrag)
screen._root.bind("<ButtonRelease-1>", exitDrag)

gen_tree((0, -400), 90, 200)

while 1:
    if not DRAGGING:
        dFORCE -= FORCE * 0.05
        FORCE = FORCE * 0.95 + dFORCE
    draw()
done()
