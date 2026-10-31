from matplotlib.pyplot import grid, plot, show, title, xlabel, ylabel
from numpy import linspace, pi, sin

R = 1.0
C = 1.5
t = linspace(0, 3, 1000)
Q_max = 1
t_s = 0.5
T = 0.8


def Q(t):
    t_c = t % T
    if t_c < t_s:
        return Q_max * sin(pi * t_c / t_s)
    else:
        return 0.0


def f(Q, P):
    return Q / C - P / R * C


Q = [Q(i) for i in t]
plot(t, Q)
xlabel("t [s]")
ylabel("Q [mL/s]")
title("Aortic flow")
grid(True)
show()
