import math
import sympy as s
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as n

t = s.Symbol('t')
x = s.sin(t)
y = s.sin(2 * t)

Vx = s.diff(x)
Vy = s.diff(y)

step = 1001
T = n.linspace(0, 10, step)
X = n.zeros_like(T)
Y = n.zeros_like(T)
VX = n.zeros_like(T)
VY = n.zeros_like(T)


for  i in n.arange(len(T)):
    X[i] = s.Subs(x, t, T[i])
    Y[i] = s.Subs(y, t, T[i])
    VX[i] = s.Subs(Vx, t, T[i])
    VY[i] = s.Subs(Vy, t, T[i])


fig = plt.figure()
axis = fig.add_subplot(1, 1, 1)
axis.axis('equal')
axis.set(xlim = [-2, 2], ylim = [-2, 2])
axis.plot(X, Y)
Pnt = axis.plot(X[0], Y[0], marker = 'o')[0]
Vp = axis.plot([X[0], X[0] + VX[0]], [Y[0], Y[0] + VY[0]])[0]


def Vect_arrow(X, Y, Valx, Valy):
    a = 0.2 
    b = 0.3
    Arx = n.array([-b, 0, -b])
    Ary = n.array([a, 0, -a])
    alpha = math.atan2(Valx, Valy)
    RotArx = Arx * n.cos(alpha) - Ary * n.sin(alpha)
    RotAry = Arx * n.sin(alpha) + Ary * n.cos(alpha)

    Arx = X + Valx + RotArx
    Ary = Y + Valy + RotAry
    return Arx, Ary


Rax, Ray = Vect_arrow(X[0], Y[0], VX[0], VY[0])
Varrow = axis.plot(Rax, Ray)[0]


def anim(i):
    Pnt.set_data(X[i], Y[i])
    Vp.set_data([X[i], X[i] + VX[i]], [Y[i], Y[i] + VY[i]])
    Rax, Ray = Vect_arrow(X[i], Y[i], VX[i], VY[i])
    Varrow.set_data(Rax, Ray)


an = FuncAnimation(fig, anim, frames=step, interval = 1)


plt.show()
