from numpy import exp, linspace, loadtxt, pi, sin
from pylab import (
    colorbar,
    imshow,
    jet,
    legend,
    plot,
    scatter,
    show,
    text,
    title,
    xlabel,
    xlim,
    ylabel,
    ylim,
)

# Grafica lineal
x1, x2 = linspace(0.0, 2.0, 20), linspace(0.0, 2.0, 200)
y1, y2, y3 = exp(-x1), exp(-x2), sin(2 * pi * x2)
y4 = y2 * y3
l1, l3, l4 = plot(x1, y1, "bD-"), plot(x2, y3, "go-"), plot(x2, y4, "rs-")
ylim(-1.1, 1.1)
xlabel("Segundos")
ylabel("Voltios")
legend((l3[0], l4[0]), ("Oscilatorio", "Amortiguado"), shadow=True)
title("Movimiento Oscilatorio Amortiguado")
show()

# Diagrama de dispersion
datos = loadtxt("stars.txt", float)
x, y = datos[:, 0], datos[:, 1]
scatter(x, y, c=x, cmap="hsv", s=75, vmin=0, vmax=14000, edgecolors="k")
xlabel("Temperatura")
ylabel("Magnitud")
xlim(13000, 0)
ylim(20, -5)
text(4500, 4.5, "Secuencia Principal", fontsize=14, style="italic")
text(11000, 15, "Enanas Blancas", fontsize=14, style="italic")
title("Diagrama Hertzsprung-Russell")
show()

# Graficas de contorno

datos = loadtxt("circular.txt", float)
imshow(datos), jet(), colorbar()
show()
