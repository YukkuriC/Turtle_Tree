__doc__ = '''递归绘制树
使用自制装饰器将原函数多线程化，并定时输出图片序列
附gif文件为将图片序列导入Photoshop制作而成
相对h7_tree.py为另一种树形'''

# 绘制函数本体所用import
from turtle import Turtle, Screen, done, tracer
from random import randint
from colorsys import hsv_to_rgb

# 导入自制装饰器与截图进程
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
    #   turtleshot(0.2, 'Tree', 'tree_realistic_%04d.png')
)
def tree_grow(turtle_pen, pos, angle, size, mode, dr):
    '''
    递归绘制一棵树
    turtle_pen : 绘制树所用turtle
    pos : 初始位置
    angle : 初始角度
    size : 树大小尺度变量
    dr : 树生长时旋转速度
    mode : 当前级别枝条种类
        0 : 花
        1 : 花条
        2 : 树枝
        3 : 树干
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
    turtle_pen.pensize(size * 2)

    # 花
    if mode == 0:
        # 随机移动一段距离并随机旋转
        turtle_pen.forward(randint(5, 10))
        turtle_pen.shapesize(randint(70, 120) / 100)
        turtle_pen.setheading(randint(1, 3600) / 10)

        # 设置随机颜色并stamp
        s = randint(30, 50) / 100
        turtle_pen.pencolor(hsv_to_rgb(0, 1 - (1 - s) * 0.8, 1))
        turtle_pen.fillcolor(hsv_to_rgb(0, s, 1))
        turtle_pen.stamp()

    # 花枝条
    elif mode == 1:
        # 合法化角度输入至(-90, 270)
        angle = (angle + 90 + 360) % 360 - 90

        # 保存每个花位置
        flowers = []

        # 绘制枝条
        turtle_pen.pendown()
        for i in range(randint(20, 40)):
            # 前进并改变角度、粗细
            turtle_pen.forward(10)
            turtle_pen.left(dr)
            turtle_pen.pensize(size * 2)
            size *= 0.97

            # 添加花朵
            flowers.append(turtle_pen.pos())
        turtle_pen.penup()

        # 向随机方向绘制所有花朵
        for p in flowers:
            tree_grow(turtle_pen, p, randint(1, 3600) / 10, 2, 0, None)

    # 中段枝条
    elif mode == 2:
        # 合法化角度至(-90, 270)区间以正常向上扭转
        angle = (angle + 90 + 360) % 360 - 90

        # 在粗细足够大时绘制枝条
        turtle_pen.pendown()
        while size > 4:
            # 前进并改变大小
            turtle_pen.forward(size)
            turtle_pen.pensize(size * 2)
            size *= 0.97

            # 朝天生长
            angle = angle + (90 - angle) * 0.1
            turtle_pen.setheading(angle)
        turtle_pen.penup()

        # 记录末端位置、角度
        p, r = turtle_pen.pos(), turtle_pen.heading()

        # 随机抽条
        for i in range(randint(3, 4)):
            tree_grow(turtle_pen, p, r + randint(-450, 450) / 10, 4, 1,
                      randint(-100, 100) / 50)

    # 树干及其分叉
    else:
        # 记录所有主干分叉
        branches = []

        # 在足够粗时绘制树干
        turtle_pen.pendown()
        while size > 6:
            # 向前旋转生长
            turtle_pen.forward(size)
            turtle_pen.left(dr)
            turtle_pen.pensize(size * 2)
            size *= 0.97

            # 树干足够细时随机改变角度并分支
            if size < 12 and randint(1, 6) == 1:
                dr = randint(-100, 100) / 10

                # 将分支位置、角度、粗细记录入列表
                branches.append((turtle_pen.pos(), randint(30, 150),
                                 size * randint(70, 90) / 100))
        turtle_pen.penup()

        # 记录末端位置、角度
        p, r = turtle_pen.pos(), turtle_pen.heading()

        # 在末端随机生长下级枝条
        for i in range(randint(1, 2)):
            tree_grow(turtle_pen, p, r + randint(-450, 450) / 10, 6, 2, None)

        # 生长所有树干分叉
        for b in branches:
            tree_grow(turtle_pen, *b, 3, randint(-100, 100) / 20)


# ============ 4. 执行 ============
# 小幅加速
tracer(10)

# 绘制树
tree_grow(new_turtle(), (0, -380), 90, 15, 3, randint(-100, 100) / 50)

# 保持窗口
done()