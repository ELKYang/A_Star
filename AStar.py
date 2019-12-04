import tkinter as tk
import numpy as np
import math
import tkinter.messagebox
import sys

# 初始化全部节点
AllNode = {}
for i in range(0, 30):
    for j in range(0, 20):
        AllNode[(i, j)] = [0, 0, 0, 0, 0,
                           0]  # F,G,H,is_obstacle,parentX,parentY

# 障碍物坐标数组
Obstacle_node_list = []
# 起点坐标
Start_node = (0, 0)
# 终点坐标
End_node = (0, 0)

# 绘制界面
window = tk.Tk()
window.title('A_Star')
window.geometry('1400x1080')
canvas = tk.Canvas(window, bg='white', width=1200, height=1080)
canvas.pack(side='left')
for i in range(0, 30):
    for j in range(0, 20):
        canvas.create_rectangle(i * 40, j * 40, i * 40 + 40, j * 40 + 40)
# 获取起始点坐标
startflag = 0


def get_start_coordinate(event):
    global startflag
    global Start_node
    if startflag == 0:
        x = math.floor(event.x / 40)
        y = math.floor(event.y / 40)
        Start_node = (x, y)
        # print('起始点坐标',Start_node)
        canvas.create_rectangle(x * 40,
                                y * 40,
                                x * 40 + 40,
                                y * 40 + 40,
                                fill='lightgreen')
        startflag = 1


# 获取障碍物坐标
def get_obstacle_coordinate(event):
    global Obstacle_node_list
    x = math.floor(event.x / 40)
    y = math.floor(event.y / 40)
    Obstacle_node_list.append((x, y))
    # print(math.floor(event.x/40),math.floor(event.y/40))
    canvas.create_rectangle(x * 40,
                            y * 40,
                            x * 40 + 40,
                            y * 40 + 40,
                            fill='grey')


# 获取终点坐标
endflag = 0


def get_end_coordinate(event):
    global endflag
    global End_node
    if endflag == 0:
        x = math.floor(event.x / 40)
        y = math.floor(event.y / 40)
        End_node = (x, y)
        # print('终止点坐标',End_node)
        canvas.create_rectangle(x * 40,
                                y * 40,
                                x * 40 + 40,
                                y * 40 + 40,
                                fill='red')
        endflag = 1


v = tk.IntVar()
v.set(None)
options = [('设置起始点', 0), ('设置障碍物', 1), ('设置终止点', 2)]


def settings():
    v.get() == 0
    if (v.get() == 0):
        canvas.bind('<Button-1>', get_start_coordinate)
    if (v.get() == 1):
        canvas.bind('<Button-1>', get_obstacle_coordinate)
    if (v.get() == 2):
        canvas.bind('<Button-1>', get_end_coordinate)


tk.Label(window, text='A星算法', font=('Times', 15)).place(x=1205, y=10)
for opt, num in options:
    tk.Radiobutton(window, text=opt, value=num, command=settings,
                   variable=v).place(x=1255, y=50 + 40 * num)


class A_star:
    def __init__(self, AllNode, Obstacle_node_list, Start_node, End_node):
        self.openlist_dict = {}  # open表
        self.closelist_dict = {}  # close表
        self.AllNode_dict = AllNode
        self.Obstacle_node_list = Obstacle_node_list  # 障碍物节点
        self.Start_node_tuple = Start_node
        self.End_node_tuple = End_node
        for x, y in self.Obstacle_node_list:
            self.AllNode_dict[(x, y)][3] = 1

# 计算F、G、H
    def calculate_F_G_H(self, x, y):
        parent_x = self.AllNode_dict[(x, y)][4]
        parent_y = self.AllNode_dict[(x, y)][5]
        parent_G = self.AllNode_dict[(parent_x, parent_y)][1]
        if x == parent_x or y == parent_y:
            self.AllNode_dict[(x, y)][1] = parent_G + 10
        if abs(x - parent_x) == 1 and abs(y - parent_y) == 1:
            self.AllNode_dict[(x, y)][1] = parent_G + 14
        self.AllNode_dict[(x, y)][2] = (abs(x - self.End_node_tuple[0]) +
                                        abs(y - self.End_node_tuple[1])) * 10
        self.AllNode_dict[(x, y)][0] = self.AllNode_dict[
            (x, y)][1] + self.AllNode_dict[(x, y)][2]

# 对相邻的方格计算G值
    def calculate_G(self, current_x, current_y, checking_x, checking_y):
        if (abs(current_x - checking_x) + abs(current_y - checking_y)) == 2:
            return 14
        else:
            return 10

# 找open表中F值最小的节点
    def find_min_F_openlist(self):
        Sort_F = []
        for key in self.openlist_dict:
            Sort_F.append((key, self.openlist_dict[key][0]))
        Sort_F = sorted(Sort_F, key=lambda x: x[1])
        (x, y) = Sort_F[0][0]
        return (x, y)

# 将节点放入open表中
    def put_into_openlist(self, node_tuple):
       #     try:
        if node_tuple[0] < 0 or node_tuple[0] > 29 or node_tuple[1] < 0 or node_tuple[1] > 19:
            return 0
        else:
            self.openlist_dict[node_tuple] = self.AllNode_dict[node_tuple]
            x = node_tuple[0]
            y = node_tuple[1]
            canvas.create_rectangle(x * 40,
                                    y * 40,
                                    x * 40 + 40,
                                    y * 40 + 40,
                                    outline="#00FFFF")
 #       except:
  #          tkinter.messagebox.showinfo(title="提示", message="无法从起始点到达终点")
   #         sys.exit()

# 将节点放入close表中
    def put_into_closelist(self, node_tuple):
        self.closelist_dict[node_tuple] = self.AllNode_dict[node_tuple]
        x = node_tuple[0]
        y = node_tuple[1]
        canvas.create_rectangle(x * 40,
                                y * 40,
                                x * 40 + 40,
                                y * 40 + 40,
                                outline='brown')

# 将节点从open表中取出
    def take_out_of_openlist(self, node_tuple):
        self.openlist_dict.pop(node_tuple)

# 检查相邻区域的节点
    def checking_adjacent_area(self, node_tuple):
        x = node_tuple[0]
        y = node_tuple[1]
        adjacent_list = [(x + 1, y), (x + 1, y - 1), (x, y - 1),
                         (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                         (x, y + 1), (x + 1, y + 1)]
        if (x + 1, y) in self.Obstacle_node_list:
            adjacent_list.remove((x + 1, y - 1))
            adjacent_list.remove((x + 1, y + 1))
        if (x, y + 1) in self.Obstacle_node_list:
            if (x + 1, y + 1) in adjacent_list:
                adjacent_list.remove((x + 1, y + 1))
        if (x, y - 1) in self.Obstacle_node_list:
            if (x + 1, y - 1) in adjacent_list:
                adjacent_list.remove((x + 1, y - 1))
        for node in adjacent_list:
            if -1 < node[0] < 30 and -1 < node[1] < 20:
                if (node not in self.Obstacle_node_list) and (
                        node not in self.closelist_dict):
                    if node not in self.openlist_dict:
                        self.put_into_openlist(node)
                        self.AllNode_dict[node][4] = x
                        self.AllNode_dict[node][5] = y
                        self.calculate_F_G_H(node[0], node[1])
                        if not node == self.Start_node_tuple:
                            canvas.create_oval(node[0] * 40 + 17.5,
                                               node[1] * 40 + 17.5,
                                               node[0] * 40 + 22.5,
                                               node[1] * 40 + 22.5)
                            # 分8中情况画箭头
                            # 右
                            if node[0] == self.AllNode_dict[node][4] - 1 and node[
                                    1] == self.AllNode_dict[node][5]:
                                canvas.create_line(node[0] * 40 + 20,
                                                   node[1] * 40 + 20,
                                                   node[0] * 40 + 30,
                                                   node[1] * 40 + 20,
                                                   tag=str(node[0]) + '__' +
                                                   str(node[1]))
                            # 右上
                            if node[0] == self.AllNode_dict[node][4] - 1 and node[
                                    1] == self.AllNode_dict[node][5] + 1:
                                canvas.create_line(node[0] * 40 + 20,
                                                   node[1] * 40 + 20,
                                                   node[0] * 40 + 30,
                                                   node[1] * 40 + 10,
                                                   tag=str(node[0]) + '__' +
                                                   str(node[1]))
                            # 上
                            if node[0] == self.AllNode_dict[node][4] and node[
                                    1] == self.AllNode_dict[node][5] + 1:
                                canvas.create_line(node[0] * 40 + 20,
                                                   node[1] * 40 + 20,
                                                   node[0] * 40 + 20,
                                                   node[1] * 40 + 10,
                                                   tag=str(node[0]) + '__' +
                                                   str(node[1]))
                            # 左上
                            if node[0] == self.AllNode_dict[node][4] + 1 and node[
                                    1] == self.AllNode_dict[node][5] + 1:
                                canvas.create_line(node[0] * 40 + 20,
                                                   node[1] * 40 + 20,
                                                   node[0] * 40 + 10,
                                                   node[1] * 40 + 10,
                                                   tag=str(node[0]) + '__' +
                                                   str(node[1]))
                            # 左
                            if node[0] == self.AllNode_dict[node][4] + 1 and node[
                                    1] == self.AllNode_dict[node][5]:
                                canvas.create_line(node[0] * 40 + 20,
                                                   node[1] * 40 + 20,
                                                   node[0] * 40 + 10,
                                                   node[1] * 40 + 20,
                                                   tag=str(node[0]) + '__' +
                                                   str(node[1]))
                            # 左下
                            if node[0] == self.AllNode_dict[node][4] + 1 and node[
                                    1] == self.AllNode_dict[node][5] - 1:
                                canvas.create_line(node[0] * 40 + 20,
                                                   node[1] * 40 + 20,
                                                   node[0] * 40 + 10,
                                                   node[1] * 40 + 30,
                                                   tag=str(node[0]) + '__' +
                                                   str(node[1]))
                            # 下
                            if node[0] == self.AllNode_dict[node][4] and node[
                                    1] == self.AllNode_dict[node][5] - 1:
                                canvas.create_line(node[0] * 40 + 20,
                                                   node[1] * 40 + 20,
                                                   node[0] * 40 + 20,
                                                   node[1] * 40 + 30,
                                                   tag=str(node[0]) + '__' +
                                                   str(node[1]))
                            # 右下
                            if node[0] == self.AllNode_dict[node][4] - 1 and node[
                                    1] == self.AllNode_dict[node][5] - 1:
                                canvas.create_line(node[0] * 40 + 20,
                                                   node[1] * 40 + 20,
                                                   node[0] * 40 + 30,
                                                   node[1] * 40 + 30,
                                                   tag=str(node[0]) + '__' +
                                                   str(node[1]))
                        if not node == self.End_node_tuple:
                            canvas.create_text(node[0] * 40 + 8,
                                               node[1] * 40 + 8,
                                               text=self.AllNode_dict[node][0],
                                               font=('Times', 8),
                                               tag=str(node[0]) + '_' +
                                               str(node[1]))
                            canvas.create_text(node[0] * 40 + 8,
                                               node[1] * 40 + 32,
                                               text=self.AllNode_dict[node][1],
                                               font=('Times', 8),
                                               tag=str(node[0]) + '_' +
                                               str(node[1]))
                            canvas.create_text(node[0] * 40 + 32,
                                               node[1] * 40 + 32,
                                               text=self.AllNode_dict[node][2],
                                               font=('Times', 8),
                                               tag=str(node[0]) + '_' +
                                               str(node[1]))
                    else:
                        if (self.AllNode_dict[node_tuple][1] +
                                    self.calculate_G(x, y, node[0], node[1])
                                ) < self.AllNode_dict[node][1]:
                            self.AllNode_dict[node][4] = x
                            self.AllNode_dict[node][5] = y
                            self.calculate_F_G_H(node[0], node[1])
                            if not node == self.Start_node_tuple:
                                canvas.delete(
                                    str(node[0]) + '__' + str(node[1]))
                                if node[0] == self.AllNode_dict[node][
                                        4] - 1 and node[1] == self.AllNode_dict[
                                            node][5]:
                                    canvas.create_line(node[0] * 40 + 20,
                                                       node[1] * 40 + 20,
                                                       node[0] * 40 + 30,
                                                       node[1] * 40 + 20,
                                                       tag=str(node[0]) + '__' +
                                                       str(node[1]))
                                if node[0] == self.AllNode_dict[node][
                                        4] - 1 and node[
                                            1] == self.AllNode_dict[node][5] + 1:
                                    canvas.create_line(node[0] * 40 + 20,
                                                       node[1] * 40 + 20,
                                                       node[0] * 40 + 30,
                                                       node[1] * 40 + 10,
                                                       tag=str(node[0]) + '__' +
                                                       str(node[1]))
                                if node[0] == self.AllNode_dict[node][4] and node[
                                        1] == self.AllNode_dict[node][5] + 1:
                                    canvas.create_line(node[0] * 40 + 20,
                                                       node[1] * 40 + 20,
                                                       node[0] * 40 + 20,
                                                       node[1] * 40 + 10,
                                                       tag=str(node[0]) + '__' +
                                                       str(node[1]))
                                if node[0] == self.AllNode_dict[node][
                                        4] + 1 and node[
                                            1] == self.AllNode_dict[node][5] + 1:
                                    canvas.create_line(node[0] * 40 + 20,
                                                       node[1] * 40 + 20,
                                                       node[0] * 40 + 10,
                                                       node[1] * 40 + 10,
                                                       tag=str(node[0]) + '__' +
                                                       str(node[1]))
                                if node[0] == self.AllNode_dict[node][
                                        4] + 1 and node[1] == self.AllNode_dict[
                                            node][5]:
                                    canvas.create_line(node[0] * 40 + 20,
                                                       node[1] * 40 + 20,
                                                       node[0] * 40 + 10,
                                                       node[1] * 40 + 20,
                                                       tag=str(node[0]) + '__' +
                                                       str(node[1]))
                                if node[0] == self.AllNode_dict[node][
                                        4] + 1 and node[
                                            1] == self.AllNode_dict[node][5] - 1:
                                    canvas.create_line(node[0] * 40 + 20,
                                                       node[1] * 40 + 20,
                                                       node[0] * 40 + 10,
                                                       node[1] * 40 + 30,
                                                       tag=str(node[0]) + '__' +
                                                       str(node[1]))
                                if node[0] == self.AllNode_dict[node][4] and node[
                                        1] == self.AllNode_dict[node][5] - 1:
                                    canvas.create_line(node[0] * 40 + 20,
                                                       node[1] * 40 + 20,
                                                       node[0] * 40 + 20,
                                                       node[1] * 40 + 30,
                                                       tag=str(node[0]) + '__' +
                                                       str(node[1]))
                                if node[0] == self.AllNode_dict[node][
                                        4] - 1 and node[
                                            1] == self.AllNode_dict[node][5] - 1:
                                    canvas.create_line(node[0] * 40 + 20,
                                                       node[1] * 40 + 20,
                                                       node[0] * 40 + 30,
                                                       node[1] * 40 + 30,
                                                       tag=str(node[0]) + '__' +
                                                       str(node[1]))
                            if not node == self.End_node_tuple:
                                canvas.delete(
                                    str(node[0]) + '_' + str(node[1]))
                                canvas.create_text(node[0] * 40 + 8,
                                                   node[1] * 40 + 8,
                                                   text=self.AllNode_dict[node][0],
                                                   font=('Times', 8),
                                                   tag=str(node[0]) + '_' +
                                                   str(node[1]))
                                canvas.create_text(node[0] * 40 + 8,
                                                   node[1] * 40 + 32,
                                                   text=self.AllNode_dict[node][1],
                                                   font=('Times', 8),
                                                   tag=str(node[0]) + '_' +
                                                   str(node[1]))
                                canvas.create_text(node[0] * 40 + 32,
                                                   node[1] * 40 + 32,
                                                   text=self.AllNode_dict[node][2],
                                                   font=('Times', 8),
                                                   tag=str(node[0]) + '_' +
                                                   str(node[1]))

# 绘制最终路径
    def paint_path(self):
        path_node = (self.AllNode_dict[self.End_node_tuple][4],
                     self.AllNode_dict[self.End_node_tuple][5])
        while not path_node == self.Start_node_tuple:
            x = path_node[0]
            y = path_node[1]
            canvas.create_oval(x * 40 + 15,
                               y * 40 + 15,
                               x * 40 + 25,
                               y * 40 + 25,
                               fill='red')
            path_node = (self.AllNode_dict[path_node][4],
                         self.AllNode_dict[path_node][5])

# A_Star核心代码
    def search(self):
        self.put_into_openlist(self.Start_node_tuple)#将初始节点放入open表中
        end_node_flag = 1
        #一直循环直至结束
        while end_node_flag:
            current_node = self.find_min_F_openlist()#将open表中F值最小的节点作为当前节点
            if -1 < current_node[0] < 30 and -1 < current_node[1] < 20:
                self.take_out_of_openlist(current_node)#将当前节点从open表中取出
                self.put_into_closelist(current_node)#将当前节点放入close表中
                self.checking_adjacent_area(current_node)#检查周围相邻节点看是否更优
                #终点出现在open list中，搜索结束，找到路径
                if self.End_node_tuple in self.openlist_dict:
                    self.paint_path()
                    tkinter.messagebox.showinfo(title="提示", message="找到路径!")
                    end_node_flag = 0
                #open list为空，搜索结束，无路径
                if not self.openlist_dict:
                    tkinter.messagebox.showinfo(title="提示", message="没有路径!")
                    end_node_flag = 0


def start():
    astar = A_star(AllNode, Obstacle_node_list, Start_node, End_node)
    astar.search()


tk.Button(window, text='Run', command=start,
          width=10, height=1).place(x=1260, y=170)
tk.Label(window, text='姓名：杨帆').place(x=1260, y=300)
tk.Label(window, text='学号：1711503').place(x=1260, y=330)
tk.Label(window, text='专业：智能科学与技术').place(x=1260, y=360)
window.mainloop()
