from math import cos, pi, sin

from numpy import arange
from vpython import canvas, color, rate, sphere, vector

L, M, N = 5, 4, 3
RNa, RCl = 0.5, 0.4
colNa, colCl = color.green, color.magenta


for k in range(-N, N + 1, 2):
    for j in range(-M, M + 1, 2):
        for i in range(-L, L + 1, 2):
            sphere(pos=vector(i, j, k), radius=RNa, color=colNa)
        for i in range(-L + 1, L + 1, 2):
            sphere(pos=vector(i, j, k), radius=RCl, color=colCl)
    for j in range(-M + 1, M + 1, 2):
        for i in range(-L, L + 1, 2):
            sphere(pos=vector(i, j, k), radius=RCl, color=colCl)
        for i in range(-L + 1, L + 1, 2):
            sphere(pos=vector(i, j, k), radius=RNa, color=colNa)

for k in range(-N + 1, N + 1, 2):
    for j in range(-M, M + 1, 2):
        for i in range(-L, L + 1, 2):
            sphere(pos=vector(i, j, k), radius=RCl, color=colCl)
        for i in range(-L + 1, L + 1, 2):
            sphere(pos=vector(i, j, k), radius=RNa, color=colNa)
    for j in range(-M + 1, M + 1, 2):
        for i in range(-L, L + 1, 2):
            sphere(pos=vector(i, j, k), radius=RNa, color=colNa)
        for i in range(-L + 1, L + 1, 2):
            sphere(pos=vector(i, j, k), radius=RCl, color=colCl)


# Movimiento

# Al parecer la nueva version de Vpython no reconoce
# x=500,y=200 y ademas center, forward y foreground
# deben ser vector, no listas

canvas(
    width=500,
    height=500,
    center=vector(0, 0, 1),
    forward=vector(0, 0, -1),
    background=color.blue,
    foreground=vector(1, 1, 0),
)
s = []
s.append(sphere(pos=vector(1, 0, 0), radius=0.25, color=color.yellow))
for theta in arange(0, 10 * pi, 0.1):
    rate(30)
    x = cos(theta)
    y = sin(theta)
    s[0].pos = vector(x, y, 0)
