import math
import sympy as s
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as n


# создаем стрелку у вектора скорости
def Vect_arrow(X, Y, Valx, Valy):
    a = 0.2 
    b = 0.3
    Arx = n.array([-b, 0, -b])
    Ary = n.array([a, 0, -a])
    alpha = math.atan2(Valy, Valx) # угол через тангенс
    RotArx = Arx * n.cos(alpha) - Ary * n.sin(alpha) # тут используем знания из линейной алгебры
    RotAry = Arx * n.sin(alpha) + Ary * n.cos(alpha) # используем матрицу поворотов

    RotArx += X + Valx
    RotAry += Y + Valy
    return RotArx, RotAry


# нужна для радиуса кривизны матрица поворота
def Rot2D(X, Y, Alpha):
    RX = X * n.cos(Alpha) - Y * n.sin(Alpha)
    RY = X * n.sin(Alpha) + Y * n.cos(Alpha)
    return RX, RY


t = s.Symbol('t')

# законы движения, которые мне даны
r = 1 + s.sin(5 * t)
phi = t

# перевод из полярных координат в декартовы
x = r * s.cos(phi)
y = r * s.sin(phi)

# считаем скорость. производная перемещения
Vx = s.diff(x)
Vy = s.diff(y)
Vmod = s.sqrt(Vx * Vx + Vy * Vy)

# считаем ускорение. производная скорости
Ax = s.diff(Vx)
Ay = s.diff(Vy)
Amod = s.sqrt(Ax * Ax + Ay * Ay) # нормальное ускорение
Atau = s.diff(Vmod) # тангенсальное ускорение

# формула для радиуса кривизны
'''
Радиус кривизны - это квадрат скорости делный на корень из расности ускорений

'''
r = (Vmod * Vmod) / s.sqrt(Amod * Amod - Atau * Atau)
w = s.diff(phi)

step = 1000
T = n.linspace(0, 10, step)
X = n.zeros_like(T)
Y = n.zeros_like(T)
VX = n.zeros_like(T)
VY = n.zeros_like(T)
AX = n.zeros_like(T)
AY = n.zeros_like(T)

R = n.zeros_like(T)
W = n.zeros_like(T)


for i in n.arange(len(T)):
    X[i] = s.Subs(x, t, T[i])
    Y[i] = s.Subs(y, t, T[i])
    VX[i] = s.Subs(Vx, t, T[i])
    VY[i] = s.Subs(Vy, t, T[i])

    # ускорение
    AX[i] = s.Subs(Ax, t, T[i])
    AY[i] = s.Subs(Ay, t, T[i])

    # вектор кривизны
    R[i] = s.Subs(r, t, T[i])
    W[i] = s.Subs(w, t, T[i])



fig = plt.figure()
axis = fig.add_subplot(1, 1, 1)
axis.axis('equal') # задали равные оси
axis.set(xlim = [-5, 5], ylim = [-5, 5]) # Настроили размер области
axis.plot(X, Y) # задачи числа на осях
Pnt = axis.plot(X[0], Y[0], marker = 'o')[0] # добавили точку на графике
Vp = axis.plot([X[0], X[0] + VX[0]], [Y[0], Y[0] + VY[0]], 'r')[0] # задали скорость на графике
Ap = axis.plot([X[0], X[0] + AX[0]], [Y[0], Y[0] + AY[0]], 'y')[0] # задали ускорение на графике
Radius = axis.plot([0, X[0]], [0, Y[0]], 'c')[0] # задали радиус на графике

Rx, Ry = Rot2D(X[0] + VX[0] / W[0], Y[0] + VY[0] / W[0], math.pi / 2)
Radius_curvate, = axis.plot([X[0], Rx], [Y[0], Ry], 'blue')


Rvx, Rvy = Vect_arrow(X[0], Y[0], VX[0], VY[0])
Varrow = axis.plot(Rvx, Rvy, 'red')[0] # отображаем стрелку на поле и окрашиваем ее в красный цвет
Rax, Ray = Vect_arrow(X[0], Y[0], AX[0], AY[0])
Aarrow = axis.plot(Rax, Ray, 'yellow')[0] # отображаем стрелку на поле и окрашиваем ее в красный цвет

# рисуем стрелку для радиуса кривизны
RArrowX, RArrowY = Vect_arrow(X[0], Y[0], Rx, Ry)
RArrow = axis.plot(RArrowX, RArrowY, 'blue')[0]

# создаем функцию для анимации
def anim(i):
    Pnt.set_data(X[i], Y[i]) # тут отображаем точку, она двигается, мы передаем раметр i
    Vp.set_data([X[i], X[i] + VX[i]], [Y[i], Y[i] + VY[i]]) # тут отображаем наши кривые
    Rvx, Rvy = Vect_arrow(X[i], Y[i], VX[i], VY[i]) # получаем данные для нашей стрелки
    Varrow.set_data(Rvx, Rvy) # отображаем стрелку в анимации
    Ap.set_data([X[i], X[i] + AX[i]], [Y[i], Y[i] + AY[i]])
    Rax, Ray = Vect_arrow(X[i], Y[i], AX[i], AY[i]) # получаем данные для нашей стрелки
    Aarrow.set_data(Rax, Ray) # отображаем стрелку в анимации

    Radius.set_data([0, X[i]], [0, Y[i]]) # строим радиус по точкам на графике
    Rx, Ry = Rot2D(VX[i] / W[i], VY[i] / W[i], math.pi / 2)
    Radius_curvate.set_data([X[i], X[i] + Rx], [Y[i], Y[i] + Ry])

    RArrowX, RArrowY = Vect_arrow(X[i], Y[i], Rx, Ry)
    RArrow.set_data(RArrowX, RArrowY)


# тут создается сама анимация
an = FuncAnimation(fig, anim, frames=step, interval=100, repeat=False)

# тут мы сохраняем анимацию в .gif
an.save('lab1.gif', fps=30, writer = 'pillow') 