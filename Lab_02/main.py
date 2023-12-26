import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math


# Блок констант
Steps = 1001
t_fin = 20
T = np.linspace(0, t_fin, Steps)
R = 5
r = 1

# Координаты цилиндр_1, по условию это точка С1
OFFSET_X_C1 = 12
OFFSET_Y_C1 = 12

# корректировка системы -> главный цилиндр опирается на цилиндр_1
l = R - 2 * r 
OC1 = l + r

# Уравнения движения
phi = 0 * np.sin(0.7 * T) + 1.1 * np.cos(2 * T) # угол для главного цилиндра и цилиндра_1
angle = 0.5 * np.sin(2.5 * T) + 1.3 * np.cos(2.5 * T)

# координаты нашей главной окружности
XO = OFFSET_X_C1 + OC1 * np.sin(phi)
YO = OFFSET_Y_C1 - OC1 * np.cos(phi)

# Координаты цилиндр_2
OFFSET_X_C2 = XO + OC1 * np.sin(angle)
OFFSET_Y_C2 = YO - OC1 * np.cos(angle)

psi = np.linspace(0, 2 * math.pi, 100) # угол для главного цилиндра и цилиндра_2

# цилиндр_1 расчет для графика
r1_X_Wheel = r * np.sin(psi)
r1_Y_Wheel = r * np.cos(psi)

# главный цилиндр расчет для графика
R_X_Wheel = R * np.sin(psi)
R_Y_Wheel = R * np.cos(psi)

# цилиндр_2 расчет для графика
r2_X_Wheel = r * np.sin(psi)
r2_Y_Wheel = r * np.cos(psi)

# Настройка графика и осей
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.axis('equal')
ax.set(xlim=[0, 25], ylim=[0, 20])


# Отображение на графике цилиндров

# Отрисовка цилиндр_1
draw_r1 = ax.plot(r1_X_Wheel + OFFSET_X_C1, r1_Y_Wheel + OFFSET_X_C1)[0]

# Отрисовка главный цилиндр
draw_R = ax.plot(R_X_Wheel + XO[0], R_Y_Wheel + YO[0])[0]

# Отрисовка цилиндр_2
draw_r2 = ax.plot(r2_X_Wheel + OFFSET_X_C2[0], r2_Y_Wheel + OFFSET_X_C2[0])[0]


# Анимация графика
def anima(i):
    draw_r1.set_data(r1_X_Wheel + OFFSET_X_C1, r1_Y_Wheel + OFFSET_X_C1)
    draw_R.set_data(R_X_Wheel + XO[i], R_Y_Wheel + YO[i])
    draw_r2.set_data(r2_X_Wheel + OFFSET_X_C2[i], r2_Y_Wheel + OFFSET_Y_C2[i])
    return [draw_r1, draw_R, draw_r2]

anim = FuncAnimation(fig, anima, frames=len(T), interval=10, repeat=True)

plt.show()
#anim.save("lab2.gif", fps=15, writer='pillow')
