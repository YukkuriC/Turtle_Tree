__doc__ = '''递归绘制树
使用自制装饰器将原函数多线程化，并定时输出图片序列
附gif文件为将图片序列导入Photoshop制作而成'''

# 绘制函数本体所用import
from turtle import Turtle, Screen, done, tracer
from random import randint
from colorsys import hsv_to_rgb
from yuulib.yturtle import TreeSplitter, turtleshot


# 创建新turtle的函数
def new_turtle():
    turtle_branch = Turtle()
    turtle_branch.hideturtle()
    turtle_branch.shape('turtle')
    turtle_branch.penup()
    turtle_branch.speed(0)
    turtle_branch.screen.delay(0)
    return turtle_branch


# 将绘制函数并行化，并挂载截图线程
# 修饰后的函数结构上仍是递归的
# 注释后还原为普通递归函数
@TreeSplitter(
    new_turtle,
    5,
    False,
    #   turtleshot(0.2, 'Tree', 'tree_%04d.png')
)
# 原函数
def tree_grow(turtle_pen, pos, angle, size, dr, size_to_branch):
    '''
    递归绘制一棵树
    turtle_pen : 绘制树所用turtle
    pos : 初始位置
    angle : 初始角度
    size : 树大小尺度变量
    dr : 树生长时旋转速度
    size_to_branch : 树大小尺度小于该值时分出枝条
    '''

    # 更新树干颜色函数
    def update_color():
        '''
        通过size决定当前色相、明度，并转化为rgb模式
        '''
        turtle_pen.color(
            hsv_to_rgb(0.04 * size / 20, 0.8, 0.2 + 0.2 * size / 20))

    # 设置初始颜色、位置、角度并落笔
    update_color()
    turtle_pen.goto(pos)
    turtle_pen.setheading(angle)
    turtle_pen.pendown()

    # 在树干足够粗时生长
    while size > 1.9:
        # 更新颜色、粗细
        update_color()
        turtle_pen.pensize(size * 2.5)

        # 向前生长并旋转
        turtle_pen.forward(size)
        turtle_pen.left(dr)

        # 在满足条件时分支
        if size < size_to_branch:
            # 记录当前位置、角度
            pos, angle = turtle_pen.pos(), turtle_pen.heading()

            # 递归反向生长树枝
            dr1 = randint(150, 250) / 50 * (-1 if dr > 0 else 1)
            size1 = size / randint(110, 130) * 100
            tree_grow(turtle_pen, pos, angle, size, dr1, size1)

            # 递归同向生长树枝
            dr2 = randint(100, 200) / 50 * (1 if dr > 0 else -1)
            size2 = size / randint(140, 160) * 100
            tree_grow(turtle_pen, pos, angle, size, dr2, size2)

            # 分裂后当前树枝停止生长
            turtle_pen.penup()
            return

        # 大小尺度衰减
        size *= 0.97

    # 若未分支则在枝端开花
    # 随机大小
    turtle_pen.penup()
    turtle_pen.shapesize(randint(80, 200) / 100)
    turtle_pen.setheading(randint(1, 3600) / 10)
    turtle_pen.color(hsv_to_rgb(0, randint(10, 40) / 100, 1))
    turtle_pen.stamp()


# ============ 4. 执行 ============
# 小幅加速
tracer(5)

# 绘制树
tree_grow(new_turtle(), (0, -400), 90, 22, randint(-100, 100) / 50, 18)

# 保持窗口
done()