import math
import sympy as s
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as n

t = s.Symbol('t')
r = 1 + s.sin(5 * t)
phi = t

x = r * s.cos(phi)
y = r * s.sin(phi)

Vx = s.diff(x)
Vy = s.diff(y)

step = 1000
T = n.linspace(0, 10, step)
X = n.zeros_like(T)
Y = n.zeros_like(T)
VX = n.zeros_like(T)
VY = n.zeros_like(T)


for i in n.arange(len(T)):
    X[i] = s.Subs(x, t, T[i])
    Y[i] = s.Subs(y, t, T[i])
    VX[i] = s.Subs(Vx, t, T[i])
    VY[i] = s.Subs(Vy, t, T[i])


fig = plt.figure()
axis = fig.add_subplot(1, 1, 1)
axis.axis('equal') # задали равные оси
axis.set(xlim = [-5, 5], ylim = [-5, 5]) # Настроили размер области
axis.plot(X, Y) # задачи числа на осях
Pnt = axis.plot(X[0], Y[0], marker = 'o')[0] # добавили точку на графике
Vp = axis.plot([X[0], X[0] + VX[0]], [Y[0], Y[0] + VY[0]], 'r')[0] # задали наши функции на графике


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


Rax, Ray = Vect_arrow(X[0], Y[0], VX[0], VY[0])
Varrow = axis.plot(Rax, Ray, 'red')[0] # отображаем стрелку на поле и окрашиваем ее в красный цвет

# создаем функцию для анимации
def anim(i):
    Pnt.set_data(X[i], Y[i]) # тут отображаем точку, она двигается, мы передаем раметр i
    Vp.set_data([X[i], X[i] + VX[i]], [Y[i], Y[i] + VY[i]]) # тут отображаем наш график
    Rax, Ray = Vect_arrow(X[i], Y[i], VX[i], VY[i]) # получаем данные для нашей стрелки
    Varrow.set_data(Rax, Ray) # отображаем стрелку в анимации


# тут создается сама анимация
an = FuncAnimation(fig, anim, frames=step, interval = 1, repeat=False)

# тут мы сохраняем анимацию в .gi
an.save("lab1.gif")
