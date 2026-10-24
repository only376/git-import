# 全屏版：跳动的粒子爱心 + 祝福便签
# 运行：python heart_fullscreen.py    按 Esc 退出
# 和小窗版的区别：窗口真全屏；心的大小、粒子数、便签尺寸全部按屏幕分辨率动态算
import math
import random
import tkinter as tk

NOTES = ["天天开心", "好运爆棚", "万事胜意", "平安喜乐", "得偿所愿",
         "早日暴富", "心想事成", "笑口常开", "前程似锦", "睡个好觉","我喜欢你"]
PASTELS = [("#fff3b0", "#6b5300"), ("#ffd6e0", "#8c2f52"),
           ("#d7f0fa", "#1e5d75"), ("#e2f6d9", "#3a6d1a"), ("#ffe4c4", "#8a4b12")]

def blend(c1, c2, f):
    """两个 #rrggbb 颜色按比例 f 混合，用来做淡入淡出"""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * f):02x}" for x, y in zip(a, b))

# ---------- 全屏窗口 ----------
root = tk.Tk()
root.attributes("-fullscreen", True)          # 真·无边框全屏（不是最大化）
cv = tk.Canvas(root, bg="black", highlightthickness=0)
cv.pack(fill="both", expand=True)
root.update_idletasks()                       # 先让窗口真实铺开，才能问到屏幕尺寸
W = max(cv.winfo_width(), root.winfo_screenwidth())
H = max(cv.winfo_height(), root.winfo_screenheight())
root.bind("<Escape>", lambda e: root.destroy())

# ---------- 按屏幕大小定标 ----------
# 心形曲线 x 跨 ±16（宽 32），y 跨 [-17, 12]（高 29），先算出"正好铺满"的缩放再留 5% 边距
SCALE = min(W / 32, H / 29) * 0.95
CX = W / 2
CY = H / 2 - 2.5 * SCALE        # 心形几何中心偏下 2.5 个单位，竖直居中要补回来

# 粒子数按屏幕面积放大，但封顶——tkinter 每帧重画上万个圆会卡
K = min((W * H) / (660.0 * 520.0), 3.0)
S = SCALE / 11.0                # 粒子半径也跟着心一起放大

# ---------- 氛围层：心后的柔光 + 全屏星星（同样"创建一次、每帧只挪"） ----------
glows = []    # (item, rx, ry)  半径单位是"心形坐标"，用时乘 SCALE
for rx, ry, color, stip in ((17.5, 16.0, "#200510", "gray12"),
                            (15.0, 13.8, "#380a1d", "gray12"),
                            (12.5, 11.5, "#4d0d26", "gray25")):
    glows.append((cv.create_oval(0, 0, 1, 1, fill=color, outline="",
                                 stipple=stip), rx, ry))

stars = []    # (x, y, s, 相位, item)  各自按自己的相位闪烁
for _ in range(90):
    x, y = random.uniform(0, W), random.uniform(0, H)
    s = random.uniform(0.7, 1.8)
    stars.append((x, y, s, random.uniform(0, 2 * math.pi),
                  cv.create_oval(x - s, y - s, x + s, y + s,
                                 fill="#282828", outline="")))

def fx(t):
    return 16 * math.sin(t) ** 3

def fy(t):
    return 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)

# 粒子改为"创建一次、每帧只挪位置"——比每帧删掉重建省一大截，帧率才提得上去
def add_particle(x, y, s, kind, r, ph):
    if kind == 0:                       # 内部：三段渐变 中心亮粉 → 玫红 → 深酒红
        if r < 0.35:
            color = blend("#ff7d9c", "#e8365f", r / 0.35)
        else:
            color = blend("#e8365f", "#6e0a1e", (r - 0.35) / 0.65)
    elif kind == 1:                     # 边缘：恒定最亮，每帧做微闪烁
        color = "#ff4d6d"
    else:                               # 光晕：跟心跳同步发光
        color = "#902030"
    item = cv.create_oval(x - s, y - s, x + s, y + s,
                          fill=color, outline="", tags="p")
    particles.append((x, y, s, kind, r, ph, item))

particles = []
for _ in range(min(int(1600 * K), 4000)):
    t = random.uniform(0, 2 * math.pi)
    r = math.sqrt(random.random())
    add_particle(CX + SCALE * fx(t) * r, CY - SCALE * fy(t) * r,
                 random.uniform(1.5, 3.5) * S, 0, r,
                 random.uniform(0, 2 * math.pi))
for _ in range(min(int(400 * K), 900)):
    t = random.uniform(0, 2 * math.pi)
    add_particle(CX + SCALE * fx(t), CY - SCALE * fy(t),
                 random.uniform(2, 4) * S, 1, 1,
                 random.uniform(0, 2 * math.pi))
for _ in range(min(int(400 * K), 900)):
    t = random.uniform(0, 2 * math.pi)
    k = random.uniform(1.03, 1.35)
    add_particle(CX + SCALE * fx(t) * k, CY - SCALE * fy(t) * k,
                 random.uniform(0.8, 1.8) * S, 2, k,
                 random.uniform(0, 2 * math.pi))

def rounded_rect_pts(x, y, hw, hh, rad, k=4):
    """圆角矩形的顶点序列：每个角取圆弧上的 k+1 个点，配合 smooth=True 画出圆角"""
    rad = max(1.0, min(rad, hw, hh))
    pts = []
    arcs = [(-math.pi / 2, x + hw - rad, y - hh + rad),   # 右上角圆心
            (0.0,          x + hw - rad, y + hh - rad),   # 右下
            (math.pi / 2,  x - hw + rad, y + hh - rad),   # 左下
            (math.pi,      x - hw + rad, y - hh + rad)]   # 左上
    for a0, ccx, ccy in arcs:
        for i in range(k + 1):
            a = a0 + (math.pi / 2) * i / k
            pts += [ccx + rad * math.cos(a), ccy + rad * math.sin(a)]
    return pts

def back_out(t):
    """easeOutBack 缓动：0 → 轻微过冲（约1.1）→ 1，弹出时带一点 Q 弹感"""
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

class Note:
    """便签：随机位置原地"弹出"，圆角 + 卷角，浮现后永久停留"""
    POP = 18   # 弹出用时（帧）

    def __init__(self):
        self.msg = random.choice(NOTES)
        self.bg, self.fg = random.choice(PASTELS)
        self.hw = max(70, W * 0.05)                       # 半宽
        self.hh = self.hw * 0.48
        self.rad = min(18, self.hh * 0.4)                 # 圆角半径
        self.f = self.rad + 6                             # 卷角大小
        self.font = max(14, int(self.hh * 0.55))
        self.x = random.uniform(self.hw + 10, W - self.hw - 10)
        self.y = random.uniform(self.hh + 10, H - self.hh - 10)
        self.age = -random.randint(0, 25)   # 负年龄 = 错峰，不会整批整齐划一地弹出
        # 注意：create_polygon 必须带初始坐标，空坐标会直接 IndexError
        self.rect = cv.create_polygon(*rounded_rect_pts(self.x, self.y, 1, 1, 1),
                                      smooth=True,
                                      fill=self.bg,
                                      outline=blend(self.bg, "#000000", 0.2), width=1)
        self.corner = cv.create_polygon(self.x, self.y, self.x, self.y, self.x, self.y,
                                        fill=blend(self.bg, "#000000", 0.3),
                                        outline="")       # 右下角卷角
        self.txt = cv.create_text(self.x, self.y, text=self.msg,
                                  font=("Microsoft YaHei", self.font, "bold"),
                                  fill=self.bg)           # 起始和底色同色 = 隐形，随弹出渐显

    def step(self):
        if self.age >= self.POP:
            return True            # 弹出完成，永久停留，不再需要每帧更新
        self.age += 1
        t = min(max(self.age / self.POP, 0.0), 1.0)
        s = back_out(t)
        if s <= 0.02:
            return True            # 还没开始长，先不画
        hw, hh, rad, f = self.hw * s, self.hh * s, self.rad * s, self.f * s
        x, y = self.x, self.y
        cv.coords(self.rect, *rounded_rect_pts(x, y, hw, hh, rad))
        cv.coords(self.corner, x + hw - f, y + hh,
                              x + hw, y + hh - f,
                              x + hw, y + hh)
        cv.itemconfig(self.txt, fill=blend(self.fg, self.bg, 1 - t))
        return True

notes = []

frame = 0
PERIOD = 90   # 一跳 ≈ 2.25 秒（40 帧/秒）

def tick():
    global frame
    frame += 1
    # "咚-哒"双峰心跳：两个高斯脉冲，强的在前、弱的在后，其余时间基本静止
    t = (frame % PERIOD) / PERIOD
    b1 = math.exp(-((t - 0.12) / 0.05) ** 2) * 0.085
    b2 = math.exp(-((t - 0.30) / 0.06) ** 2) * 0.050
    beat = 1 + b1 + b2
    glow = min(1.0, (b1 + b2) * 9)          # 0~1 的发光强度，和心跳同相
    # 背景柔光跟着心跳呼吸
    for item, rx, ry in glows:
        cv.coords(item, CX - rx * SCALE * beat, CY - ry * SCALE * beat,
                        CX + rx * SCALE * beat, CY + ry * SCALE * beat)
    # 星星各自闪烁：sin³ 让它们大部分时间暗、偶尔亮一下
    for x, y, s, ph, item in stars:
        tw = 0.5 + 0.5 * math.sin(frame / 11 + ph)
        v = int(40 + 200 * tw ** 3)
        cv.itemconfig(item, fill=f"#{v:02x}{int(v * 0.88):02x}{int(v * 0.94):02x}")
    for x, y, s, kind, r, ph, item in particles:
        px, py = CX + (x - CX) * beat, CY + (y - CY) * beat
        cv.coords(item, px - s, py - s, px + s, py + s)
        if kind == 1:         # 边缘：各自的相位微微闪烁
            f = 0.78 + 0.22 * math.sin(frame / 7 + ph)
            cv.itemconfig(item, fill=f"#{int(255 * f):02x}{int(77 * f):02x}{int(109 * f):02x}")
        elif kind == 2:       # 光晕：心跳瞬间整体亮起，平时暗下去
            f = min(1.0, 0.30 + 0.70 * glow * (0.6 + 0.4 * math.sin(ph + frame / 9)))
            cv.itemconfig(item, fill=f"#{int(176 * f):02x}{int(37 * f):02x}{int(69 * f):02x}")
    # 分 5 批随机弹出；一批 ~26 张，5 批共 ~130 张差不多铺满全屏
    if frame in (15, 55, 95, 135, 175):
        for _ in range(random.randint(24, 28)):
            notes.append(Note())
    notes[:] = [n for n in notes if n.step()]
    cv.after(25, tick)        # 40 帧/秒；粒子改成"只挪不重建"才撑得住

tick()
root.mainloop()
