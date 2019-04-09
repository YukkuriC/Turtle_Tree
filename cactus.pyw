from yuulib.yturtle import TreeSplitter, turtleshot
import turtle, random, colorsys


def new_turtle():
    turtle_branch = turtle.Pen()
    turtle_branch.hideturtle()
    turtle_branch.shape('turtle')
    turtle_branch.fillcolor('green')
    turtle_branch.penup()
    turtle_branch.speed(0)
    turtle_branch.screen.delay(0)
    return turtle_branch


@TreeSplitter(
    new_turtle,
    5,
    # helper_func=turtleshot(0.1, 'Tree', 'cactus_%04d.jpg')
)
def tentacle_grow(turtle_pen, pos, angle, size, size_to_branch, side):
    def update_color():
        turtle_pen.pencolor(
            colorsys.hsv_to_rgb(0.333, 0.6, 0.3 - 0.1 * size / 20))

    update_color()
    turtle_pen.goto(pos)
    turtle_pen.setheading(angle)
    turtle_pen.pensize(size * 1.5)
    turtle_pen.pendown()
    while size > 2:
        update_color()
        turtle_pen.pensize(size + 6)
        turtle_pen.forward(size)
        angle = angle + (90 - angle) / 5
        turtle_pen.setheading(angle)
        # 分支
        if size < size_to_branch:
            pos = turtle_pen.pos()
            tentacle_grow(turtle_pen, pos, 0 if side == 1 else 180,
                          size / random.randint(110, 130) * 100, size / 2.4,
                          random.randrange(2) * 2 - 1)
            side *= -1
            size_to_branch = size / 1.4
            turtle_pen.goto(pos)
            turtle_pen.setheading(angle)
            turtle_pen.pendown()
        # 衰减
        size *= 0.97

    turtle_pen.penup()


tentacle_grow(new_turtle(), (0, -350), 90, 20, 18, random.randrange(1) * 2 - 1)
turtle.done()