from turtle import Pen, done
from math import sin, cos, pi
from functools import lru_cache
from random import randrange

MAX_LAYER = 10


def locate_pos(layer, ind):
    span = pi * (layer / 100 + 1)
    angle = (pi - span) / 2 + span * (0.5 + ind) / layer
    r = (layer - 1) * 50
    return r * cos(angle), r * sin(angle) - 150


@lru_cache(None)
def calc_pascal(layer, ind):
    if ind < 0 or ind >= layer:
        return 0
    if layer == 1:
        return 1
    return calc_pascal(layer - 1, ind) + calc_pascal(layer - 1, ind - 1)


t_branch = Pen('circle')
t_branch.penup()
t_branch.speed(0)
t_branch.screen.delay(0)
t_branch.color('black', 'white')
t_branch.shapesize(2)
t_branch.hideturtle()

t_text = t_branch.clone()
t_text.color('red')

t_koch = t_branch.clone()


def draw_branch(root, layer, ind, expand=True):
    new_root = locate_pos(layer, ind)

    t_branch.goto(root)
    t_branch.pendown()
    t_branch.goto(new_root)
    t_branch.penup()

    if layer < MAX_LAYER and expand:
        draw_branch(new_root, layer + 1, ind, ind == 0)
        draw_branch(new_root, layer + 1, ind + 1)


def draw_pascal(layer):
    if layer < MAX_LAYER:
        for ind in range(layer):
            pos = locate_pos(layer, ind)
            t_branch.goto(pos)
            t_branch.stamp()
            t_text.goto(pos[0], pos[1] - 20)
            t_text.write(
                calc_pascal(layer, ind),
                align='center',
                font=('comic sans ms', 20, 'normal'))
        draw_pascal(layer + 1)
    else:
        for ind in range(layer):
            pos = locate_pos(layer, ind)
            draw_koch_flake(pos)


def draw_koch(size, layer):
    if layer <= 1:
        return t_koch.forward(size)
    for r in 60, -120, 60, 0:
        draw_koch(size / 3, layer - 1)
        t_koch.left(r)


def draw_koch_flake(pos):
    t_koch.goto(pos)
    t_koch.setheading(randrange(360))
    size = 40
    t_koch.forward(size)
    t_koch.right(150)
    size *= 3**0.5
    t_koch.pendown()
    t_koch.begin_fill()
    for i in range(3):
        draw_koch(size, 5)
        t_koch.right(120)
    t_koch.penup()
    t_koch.end_fill()


draw_branch((0, -400), 1, 0)
draw_pascal(1)
done()