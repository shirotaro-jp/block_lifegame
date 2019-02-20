# ブロック崩し
from tkinter import *
import random
import numpy as np
import time

# ゲーム中で使う変数の一覧
blocks = []
block_size = {"x": 25, "y": 25}
ball = {"dirx": 15, "diry": -15, "x": 350, "y": 300, "w": 10}
bar = {"x": 0, "w": 100}
is_gameover = False
point = 0
row = 6
column = 24
state = np.zeros((row,column), dtype=np.int8)
next_state = np.empty((row,column), dtype=np.int8)
start_time = ""
game_time = ""

# ウィンドウの作成
win = Tk()
cv = Canvas(win, width = 600, height = 400)
cv.pack()

# ゲームの初期化
def init_game():
    global is_gameover, point, row, column, start_time, game_time
    is_gameover = False
    game_time = ""
    start_time = time.time()
    ball["y"] = 250
    ball["diry"] = -10
    point = 0
    # ブロックを配置する
    for iy in range(0, row):
        for ix in range(0, column):
            state[iy, ix] = random.randint(0, 1)
            color = "red"
            if (iy + ix) % 2 == 1: color = "blue"
            x1 = 4 + ix * block_size["x"]
            x2 = x1 + block_size["x"]
            y1 = 4 + iy * block_size["y"]
            y2 = y1 + block_size["y"]
            blocks.append([x1, y1, x2, y2, color, iy, ix])
    win.title("START")

# オブジェクトを描画する
def draw_objects():
    cv.delete('all') # 既存の描画を破棄
    cv.create_rectangle(0, 0, 600, 400, fill="black", width=0)
    # ブロックを一つずつ描画
    for w in blocks:
        x1, y1, x2, y2, c ,iy, ix = w
        if state[iy,ix] == 1: cv.create_rectangle(x1, y1, x2, y2, fill=c, width=0)
    # ボールを描画
    cv.create_oval(ball["x"] - ball["w"], ball["y"] - ball["w"],
        ball["x"] + ball["w"], ball["y"] + ball["w"], fill="green")
    # バーを描画
    cv.create_rectangle(bar["x"], 390, bar["x"] + bar["w"], 400, 
        fill="yellow")

# ボールの移動
def move_ball():
    global is_gameover, point, game_time
    if is_gameover: return
    bx = ball["x"] + ball["dirx"]
    by = ball["y"] + ball["diry"]
    # 上左右の壁に当たった？
    if bx < 0 or bx > 600: ball["dirx"] *= -1
    if by < 0: ball["diry"] *= -1
    # プレイヤーの操作するバーに当たった？
    if by > 390 and (bar["x"] <= bx <= (bar["x"] + bar["w"]/3)):
        life_game()
        ball["diry"] *= -1
        if ball["dirx"] >= 0: ball["dirx"] *= -1
        by = 380
    elif by > 390 and ((bar["x"] + bar["w"]/3) <= bx <= (bar["x"] + bar["w"]/3*2)):
        life_game()
        ball["diry"] *= -1
        by = 380
    elif by > 390 and ((bar["x"] + bar["w"]/3*2) <= bx <= (bar["x"] + bar["w"])):
        life_game()
        ball["diry"] *= -1
        if ball["dirx"] <= 0: ball["dirx"] *= -1
        by = 380
    # ボールがブロックに当たった？
    # hit_i = -1
    for i, w in enumerate(blocks):
        x1, y1, x2, y2, color, iy, ix = w
        w3 = ball["w"] / 3
        if state[iy,ix] == 1:
            if (x1-w3 <= bx <= x2+w3) and (y1-w3 <= by <= y2+w3):
                state[iy,ix] = 0
                if random.randint(0, 1) == 0: ball["dirx"] *= -1
                ball["diry"] *= -1
                point += 10
                win.title("GAME SCORE = " + str(point))
                break
    # ゲームオーバー？
    if by >= 400:
        if game_time == "":
            win.title("Game Over!! score=" + str(point))
            is_gameover = True
    if 0 <= bx <= 600: ball["x"] = bx
    if 0 <= by <= 400: ball["y"] = by

def life_game():
    global is_gameover, row, column, state, next_state
    # ライフゲーム
    for i in range(0, row):
        for j in range(0, column):
            # 自分と近傍のセルの状態を取得
            # c: center (自分自身)
            # nw: north west, ne: north east, c: center ...
            nw = state[i-1,j-1]
            n  = state[i-1,j]
            ne = state[i-1,(j+1)%column]
            w  = state[i,j-1]
            c  = state[i,j]
            e  = state[i,(j+1)%column]
            sw = state[(i+1)%row,j-1]
            s  = state[(i+1)%row,j]
            se = state[(i+1)%row,(j+1)%row]
            neighbor_cell_sum = nw + n + ne + w + e + sw + s + se
            if c == 0 and neighbor_cell_sum == 3:
                next_state[i,j] = 1
            elif c == 1 and neighbor_cell_sum in (2,3):
                next_state[i,j] = 1
            else:
                next_state[i,j] = 0
    state, next_state = next_state, state
    # ブロックを一つずつ描画
    for w in blocks:
        x1, y1, x2, y2, c ,iy, ix = w
        if state[iy,ix] == 1:
            cv.create_rectangle(x1, y1, x2, y2, fill=c, width=0)

def game_clear():
    global is_gameover, game_time
    if np.any(state) != True:
        if game_time == "":
            clear_time = time.time()
            game_time = clear_time - start_time
            game_time = int(game_time)
            win.title("Clear the game!! score=" + str(point) + " time=" + str(game_time) + "s")
            is_gameover = True

def game_loop():
    game_clear()
    draw_objects()
    move_ball()
    win.after(50, game_loop)

# マウスイベントの処理
def motion(e): # マウスポインタの移動
    bar["x"] = e.x
def click(e): # クリックでリスタート
    if is_gameover: init_game()
# マウスイベントを登録
win.bind('<Motion>', motion)
win.bind('<Button-1>', click)
# ゲームのメイン処理
init_game()
game_loop()
win.mainloop()

