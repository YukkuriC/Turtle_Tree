import turtle, random, math
from yuulib.yturtle import TreeSplitter, turtleshot


def tt_gen():
    tt = turtle.Pen()
    tt.speed(0)
    tt.screen.delay(0)
    tt.penup()
    tt.setposition(0, -400)
    tt.hideturtle()
    tt.shape('circle')
    return tt


def leaf(tt, color, size):
    tt.pencolor(color)
    tt.fillcolor(color)
    tt.shapesize(size)
    tt.stamp()


@TreeSplitter(
    tt_gen,
    15,
    # helper_func=turtleshot(0.5, 'Tree', 'tree_%04d.jpg')
)
def tree(tt, pos, size, angle, floor):
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
            tree(tt, pp, size - 10, angle + random.randint(-15 * i, 15 * i),
                 floor - 1)
        if random.randint(0, 30) < 10:
            leaf(tt,
                 (random.randint(10, 30) * 0.01, random.randint(60, 80) * 0.01,
                  random.randint(20, 40) * 0.01),
                 random.randint(10, 20) * 0.1)
    else:
        leaf(tt, (random.randint(10, 30) * 0.01, random.randint(60, 80) * 0.01,
                  random.randint(20, 40) * 0.01),
             random.randint(40, 50) * 0.1)
    tt.setheading(angle + 180)
    tt.forward(size)


tree(tt_gen(), (0, -400), 135, 90, 5)
turtle.done()
