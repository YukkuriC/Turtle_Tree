from yuulib.yturtle import TreeSplitter
import turtle, random, colorsys, math


def new_turtle():
    turtle_branch = turtle.Pen()
    turtle_branch.hideturtle()
    turtle_branch.shape('turtle')
    turtle_branch.fillcolor('green')
    turtle_branch.penup()
    turtle_branch.speed(0)
    turtle_branch.screen.delay(0)
    return turtle_branch


@TreeSplitter(new_turtle, 5, False)
def spring_grow(turtle_pen, pos, angle, length, size, dr, phase=0):
    def locate():
        offset = turtle.Vec2D(size * math.cos(phase * 3.1416 / 180),
                              3 * size * math.sin(phase * 3.1416 / 180))
        turtle_pen.goto(pos + offset.rotate(angle))

    dist = 0
    pos = turtle.Vec2D(*pos)
    locate()
    turtle_pen.setheading(angle)
    turtle_pen.pendown()
    while dist < length:
        pos += turtle.Vec2D(size/30+0.2, 0).rotate(angle)
        dist += size/30+0.2
        angle += dr
        locate()
        phase += size
        # 衰减
        size *=0.998

    turtle_pen.penup()
    if length>10 and size>1.5:
        spring_grow(turtle_pen, pos, angle, length-5, size,
                    random.randint(-250, 250) / 1000, phase)
        spring_grow(turtle_pen, pos, angle, length-10, size,
                    random.randint(-250, 250) / 1000, phase)
    else:
        turtle_pen.shapesize(random.randint(80, 200) / 100)
        turtle_pen.setheading(random.randint(1, 3600) / 10)
        turtle_pen.fillcolor(colorsys.hls_to_rgb(random.randrange(3600)/3600,0.5,1))
        turtle_pen.stamp()

turtle.tracer(10)
spring_grow(new_turtle(), (0, -400), 90, 150, 25, 0)
turtle.done()