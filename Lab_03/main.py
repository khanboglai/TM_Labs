import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from scipy.integrate import odeint


# функция для решения диффуров
def odesys(y, t, m1, m2, a, b, g):
    dy = np.zeros(4)
    dy[0] = y[2]
    dy[1] = y[3]

    # система в общем виде
    a11 = 2 * a * (m1 + m2)
    a12 = -1 * m2 * b * (1 - np.cos(y[1] - y[0]))
    a21 = a * (1 - np.cos(y[1] - y[0]))
    a22 = -2 * b

    b1 = m2 * b * np.sin(y[1] - y[0]) * (y[3] ** 2) - g * (m1 + m2) * np.sin(y[0])
    b2 = a * np.sin(y[1] - y[0]) * (y[2] ** 2) + g * np.sin(y[1])

    dy[2] = (b1 * a22 - b2 * a12) / (a11 * a22 - a12 * a21)
    dy[3] = (b2 * a11 - b1 * a21) / (a11 * a22 - a12 * a21)

    return dy


# блок констант из условия
m1 = 4
m2 = 2
r1 = 1
r2 = 0.125
r3 = 0.05
g = 9.81 # ускорение свободного падения

phi0 = np.pi / 6
psi0 = np.pi / 3
dphi0 = 0
dpsi0 = np.pi / 3

# константы из условия
a = r1 - r3
b = r1 - r2


Steps = 1001
t_fin = 20
t = np.linspace(0, t_fin, Steps)

y0 = [phi0, psi0, dphi0, dpsi0] # начальные условия

Y = odeint(odesys, y0, t, (m1, m2, a, b, g))

phi = Y[:, 0]
psi = Y[:, 1]

# расчет производных
dphi = Y[:, 2]
dpsi = Y[:, 3]
ddphi = [odesys(y, t, m1, m2, a, b, g)[2] for y, t in zip(Y, t)]
ddpsi = [odesys(y, t, m1, m2, a, b, g)[3] for y, t in zip(Y, t)]

# нормаьная реакция 
N1 = (m1 + m2) * (g * np.cos(phi) + a * dphi ** 2) + m2 * b * (ddpsi * np.sin(psi - phi) + np.cos(psi - phi) * dpsi ** 2)

# сила трения
Ftr = (m1 + m2) * (g * np.sin(phi) + a * np.square(ddphi)) + m2 * b * (ddpsi * np.cos(psi-phi) - np.sin(psi-phi) * np.square(dpsi))


# Отображение зависимостей из условия
fig_graphs = plt.figure(figsize=[13, 7])
axis_graphs = fig_graphs.add_subplot(2, 2, 1)
axis_graphs.plot(t, phi, color='Blue')
axis_graphs.set_title("phi(t)")
axis_graphs.set(xlim =[0, t_fin])
axis_graphs.grid(True)

axis_graphs = fig_graphs.add_subplot(2, 2, 3)
axis_graphs.plot(t, psi, color='Red')
axis_graphs.set_title("psi(t)")
axis_graphs.set(xlim =[0, t_fin])
axis_graphs.grid(True)

axis_graphs = fig_graphs.add_subplot(2, 2, 2)
axis_graphs.plot(t, N1, color='Green')
axis_graphs.set_title("N1(t)")
axis_graphs.set(xlim =[0, t_fin])
axis_graphs.grid(True)

axis_graphs = fig_graphs.add_subplot(2, 2, 4)
axis_graphs.plot(t, Ftr, color='Purple')
axis_graphs.set_title("Ftr(t)")
axis_graphs.set(xlim =[0, t_fin])
axis_graphs.grid(True)

fig_graphs.savefig("lab3.jpg")

# отрисовка из лр 2, но с другими параметрами
OFFSET_X_C1 = 3
OFFSET_Y_C1 = 3

l1 = r1 - 2 * r3
l2 = r1 - 2 * r2
OC1 = l1 + r3
OC2 = l2 + r2 

XO = OFFSET_X_C1 + OC1 * np.sin(phi)
YO = OFFSET_Y_C1 - OC1 * np.cos(phi)
OFFSET_X_C2 = XO + OC2 * np.sin(psi)
OFFSET_Y_C2 = YO - OC2 * np.cos(psi)

psi = np.linspace(0, 2 * math.pi, 100)

r1_X_Wheel = r3 * np.sin(psi)
r1_Y_Wheel = r3 * np.cos(psi)

R_X_Wheel = r1 * np.sin(psi)
R_Y_Wheel = r1 * np.cos(psi)

r2_X_Wheel = r2 * np.sin(psi)
r2_Y_Wheel = r2 * np.cos(psi)


# Построение графика для системы
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.axis('equal')
ax.set(xlim=[0, 5], ylim=[0, 5])

# Отображение на графике
draw_r1 = ax.plot(r1_X_Wheel + OFFSET_X_C1, r1_Y_Wheel + OFFSET_X_C1)[0]
draw_R = ax.plot(R_X_Wheel + XO[0], R_Y_Wheel + YO[0])[0]
draw_r2 = ax.plot(r2_X_Wheel + OFFSET_X_C2[0], r2_Y_Wheel + OFFSET_X_C2[0])[0]


# Анимация
def anima(i):
    draw_r1.set_data(r1_X_Wheel + OFFSET_X_C1, r1_Y_Wheel + OFFSET_X_C1)
    draw_R.set_data(R_X_Wheel + XO[i], R_Y_Wheel + YO[i])
    draw_r2.set_data(r2_X_Wheel + OFFSET_X_C2[i], r2_Y_Wheel + OFFSET_Y_C2[i])
    return [draw_r1, draw_R, draw_r2]

anim = FuncAnimation(fig, anima, frames=len(t), interval=10, repeat=False)

plt.show()
#anim.save("lab3.gif", fps=15, writer='pillow')
