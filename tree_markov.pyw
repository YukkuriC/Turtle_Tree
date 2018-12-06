from turtle import Turtle, Screen, tracer, done
from random import randint
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

__doc__ = '''递归绘制马尔可夫树
由文本统计生成转移频率，再根据概率生成树
支持直接输入及选择文件方式输入文本'''

# ============ 1. 初始化 ============
### 全局控制变量
MINL = 20  # 最短树枝长度
MAXSPAN = 70  # 最宽左右角度分布（180以下）
MINFONT = 15  # 最小节点字号
STRAIGHT_REDUCTION = 0.96  # 直链传导时强度衰减（小于1）
MIN_BRANCH_STR = 1  # 最小生成树枝强度
MIN_ROOT_STR = 1.5  # 最小生成树根强度
BULLETSYM = '#'  # 项目符号
COLOR_BRANCH = 'black'  # 树干树枝颜色
COLOR_NODE = 'green'  # 树枝节点颜色
COLOR_ROOT = 'blue'  # 树根生成文字颜色

### 绘图接口初始化
t = Turtle()
t.pu()
t.speed(0)
t.screen.delay(0)
t.setundobuffer(None)
t.hideturtle()
nodes = []

### 窗口句柄获取
screen = Screen()
tk = screen._root


# ============ 2. 单元函数定义 ============
### 生成字典树部分
def gen_dict(text, append=False):
    '''
    根据输入文字生成转移字典trans
    text : 输入文字
    append : 是否往现有字典添加而非新建，默认为否
    '''
    # 初始化字典
    global trans
    try:
        assert append  # 在append为假时直接报错
        trans.get('#')  # 确保对象存在
    except:
        trans = {}  # 接到报错时新建空字典

    # 逐个添加前后字符映射
    for i in range(len(text) - 1):
        prv, nxt = text[i], text[i + 1]
        if not prv in trans:  # 原本无前字符则新建字典
            trans[prv] = {}
        trans[prv][nxt] = trans[prv].get(nxt, 0) + 1  # 计数增加


def branch(pos, angle, content, anglespan, l, strength):
    '''
    调用turtle对象t进行树枝绘制，并递归生成树根
    pos : 树枝底部位置
    angle : 树枝生长角度
    content : 该树枝内容
    anglespan : 枝端发散范围（左右）
    l : 树枝长度
    strength : 传播强度
    '''
    # 若强度过低则不生成树枝
    if strength < MIN_BRANCH_STR:
        return

    # 初始化位置角度粗细
    t.goto(pos)
    t.setheading(angle)
    t.pensize(strength**0.5)

    # 绘制树枝
    t.pd()
    t.forward(l)
    t.pu()

    # 向全局列表nodes中添加枝端位置、内容、强度
    nodes.append((t._position, content, strength))

    # 若强度够大则
    if strength > MIN_ROOT_STR:
        root(t._position, angle, content, anglespan, l, strength)


def root(pos, angle, content, anglespan, l, size):
    '''
    由新的树根生成次级传播树枝
    pos : 树根位置
    angle : 树根中心角度
    content : 该树根内容
    anglespan : 树根发散范围（左右）
    l : 树根基础长度
    size : 传播强度（树根大小）
    '''
    # 若字典中无内容则无树枝生成
    if not content in trans:
        return

    # 获取字典键/值列表
    k, v = list(trans[content].keys()), list(trans[content].values())

    # 根据值等比例为每个键分配角度区间
    ratio = anglespan * 2 / sum(v)
    pts = [angle - anglespan]
    for i in v:
        pts.append(pts[-1] + ratio * i)

    # 根据角度区间递归绘制下级树枝
    for i in range(len(k)):
        angle_new = (pts[i + 1] + pts[i]) / 2  # 树枝角度为区间中点
        anglespan_new = (
            pts[i + 1] - pts[i]) / 2  # 角度范围为区间半长度，为美观考虑扩大以sqrt(字典大小)
        anglespan_new = min(MAXSPAN, anglespan_new * (len(k)**0.75))
        l_new = max(l + 20 - 30 * (anglespan_new / anglespan),
                    MINL)  # 小概率分支长度更大
        strength_new = size * v[i] / sum(v)  # 按权重分配强度，大概率分支强度更大
        if len(v) == 1:  # 单分支时强度衰减，避免无限递归
            strength_new *= STRAIGHT_REDUCTION
        branch(pos, angle_new, k[i], anglespan_new, l_new,
               strength_new)  # 生成树枝


def draw_nodes():
    '''
    统一绘制所有枝端节点内容
    '''
    for n in nodes:
        size = int(max(MINFONT, n[2]**0.5))  # 确定字体大小
        t.goto(n[0][0], n[0][1] - size * 0.4)  # 微调中心以将字符放于节点处
        t.write(n[1], align='center', font=('微软雅黑', size, 'normal'))  # 绘制节点内容


def gen_tree():
    '''
    根据当前转移字典trans内容生成树
    '''
    # 清空节点列表
    global nodes
    nodes = []

    # 递归生成树
    t.color(COLOR_BRANCH)
    branch((0, -400), 90, '#', MAXSPAN, 100, 1000)

    # 绘制节点内容
    t.color(COLOR_NODE)
    draw_nodes()


### 窗口句柄部分
def pack_components():
    '''
    初始化操作界面
    在tkinter窗口中组装必要部件
    '''
    ### 直接输入模块
    global input_text, gen_button, append_button
    input_part = Frame(tk)
    input_part.pack(fill=X)

    # 文本输入框
    Label(input_part, text=BULLETSYM).pack(side=LEFT)  # 项目符号
    input_content = StringVar(value='吃葡萄不吐葡萄皮不吃葡萄倒吐葡萄皮')
    input_text = Entry(input_part, textvariable=input_content)
    input_text.content = input_content  # 变量附加至主体

    # 控制按钮
    gen_button = Button(
        input_part, text='生成新字典树', command=lambda: gen_button_action(False))
    append_button = Button(
        input_part, text='续接字典树', command=lambda: gen_button_action(True))

    # 装配控件
    append_button.pack(padx=5, side=RIGHT)
    gen_button.pack(padx=5, side=RIGHT)
    input_text.pack(padx=5, fill=X)

    ### 文件选择模块
    global file_path, select_button, read_button
    file_part = Frame(tk)
    file_part.pack(pady=5, fill=X)

    # 显示文档选择路径
    Label(file_part, text='选择文件').pack(side=LEFT)
    file_content = StringVar(value='')
    file_path = Entry(file_part, textvariable=file_content)
    file_path.content = file_content  # 变量附加至主体

    # 控制按钮
    select_button = Button(file_part, text='浏览...', command=browse_file)
    read_button = Button(file_part, text='从文件生成', command=gen_from_file)

    # 装配控件
    read_button.pack(padx=5, side=RIGHT)
    select_button.pack(padx=5, side=RIGHT)
    file_path.pack(padx=5, fill=X)

    ### 全局声明列表存放所有可操作控件
    global op_list
    op_list = [
        input_text, gen_button, append_button, file_path, select_button,
        read_button
    ]


def gen_button_action(append):
    '''
    以输入文本初始化字典并生成树
    append : 是否为续接到现有字典后
    '''
    # 生成字典
    text = BULLETSYM + input_text.content.get()
    gen_dict(text, append)

    # 更新树根显示文字
    try:
        assert append
        gen_button_action.text += '\n' + text
    except:
        gen_button_action.text = text

    # 关闭所有控件以防误触
    for i in op_list:
        i['state'] = DISABLED

    # 清空屏幕并绘制树
    screen._delete("all")
    gen_tree()

    # 显示根部文字
    t.color(COLOR_ROOT)
    t.goto(0, -350)
    t.write(gen_button_action.text, align='center', font=('微软雅黑', 15, 'bold'))

    # 重新开启控件
    for i in op_list:
        i['state'] = NORMAL


def browse_file():
    '''
    浏览计算机获取文件路径
    '''
    path = askopenfilename()
    if path:
        file_path.content.set(path)


def gen_from_file():
    '''
    从选定文件路径读取文件生成树
    '''
    # 打开文件
    try:
        file = open(file_path.content.get(), encoding='utf-8')
    except FileNotFoundError:
        showerror('错误', '文件不存在')
        return browse_file()

    # 读取内容
    try:
        content = file.read()
    except UnicodeDecodeError:
        showerror('错误', '格式不支持')
        return browse_file()

    # 生成字典
    gen_dict(BULLETSYM + content)

    # 关闭所有控件以防误触
    for i in op_list:
        i['state'] = DISABLED

    # 清空屏幕并绘制树
    screen._delete("all")
    gen_tree()

    # 根部显示文件目录
    t.color(COLOR_ROOT)
    t.goto(0, -350)
    t.write(
        BULLETSYM + ' ' + file_path.content.get(),
        align='center',
        font=('微软雅黑', 15, 'bold'))

    # 重新开启控件
    for i in op_list:
        i['state'] = NORMAL


tk.title('马尔可夫树')
pack_components()
done()
