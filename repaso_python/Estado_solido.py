import warnings

# Esto silencia un mensaje de error que sale en la terminal al ejecutar el programa, pero no afecta a la visualización de la escena.
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

from itertools import product
from math import cos, radians, sin

from vpython import button, canvas, color, curve, cylinder, rate, sphere, vector

# --------------------------------------------------------------------------------------------------------------------------

a = 1.0  # parámetro de red
r_atomo = 0.08 * a
r_enlace = 0.02 * a
eps = 1e-6

# Base de la red FCC (en unidades de a) y desplazamiento de la subred B
FCC = [vector(0, 0, 0), vector(0.5, 0.5, 0), vector(0.5, 0, 0.5), vector(0, 0.5, 0.5)]
desp = vector(0.25, 0.25, 0.25)
AZUL = vector(0.12, 0.37, 0.66)  # subred A
AMBAR = vector(0.79, 0.54, 0.02)  # subred B


def usuario():
    # Esta función pregunta al usuario qué red quiere ver y
    # cuántas celdas dibujar.
    TITULOS = {
        "d": "ESTRUCTURA DE DIAMANTE",
        "h": "RED HEXAGONAL COMPACTA (HCP)",
        "f": "RED CÚBICA CENTRADA EN LAS CARAS (FCC)",
    }

    red = ""
    while red not in TITULOS:
        red = (
            input(
                "¿Qué tipo de red quieres visualizar? "
                "(Diamante == d, Hexagonal == h o FCC == f): "
            )
            .strip()  # quita los espacios en blanco (y saltos de línea o tabuladores) del principio y del final del texto
            .lower()  # pasa todo el texto a minusculas
        )

    N = 0
    while N < 1:
        try:
            N = int(
                input("Introduce el número de celdas a dibujar (entero positivo): ")
            )
        except ValueError:
            N = 0  # no era un número entero; se vuelve a preguntar

    return red, N, TITULOS[red]


red, N, titulo = usuario()


def dentro(p):
    # Esta funcion comprueba si un punto cae dentro del
    # bloque [0, N]^3 (bordes incluidos).
    # Dado un vector p = (p_x,p_y,p_z) el comando
    # p.x accede a la primer valor, p_x
    return all(-eps <= c <= N + eps for c in (p.x, p.y, p.z))


scene = canvas(
    # Esto establece como es la escena, el tamaño, el color de
    # fondo y el titulo del programa.
    title=f'<b style="font-size:28px">{titulo}</b>',
    width=900,
    height=650,
    background=color.white,
)
scene.center = vector(N / 2, N / 2, N / 2) * a

# RED DE DIAMANTE (d)

if red == "d":
    # range de -1 a N+1 suena raro pero es porque range no coge el uñtimo numero
    # asique esta contado de -1 a N y el -1 es por si acaso, aunque con las
    # bases que manejo estos puntos siempe caen fuera de la red
    for i, j, k in product(range(-1, N + 1), repeat=3):
        # este bucle da 4 vueltas y asigna cada valor de la base FCC
        # a b para dibujar cada atomo de la base
        for b in FCC:
            p = vector(i, j, k) + b  # átomo de la subred A
            if dentro(p):
                sphere(pos=p * a, radius=r_atomo, color=AZUL)

            q = p + desp  # átomo de la subred B
            if dentro(q):
                sphere(pos=q * a, radius=r_atomo, color=AMBAR)
                # Sus 4 vecinos A están en p, p+(½,½,0), p+(½,0,½), p+(0,½,½),
                # todos a distancia a·√3/4 y formando un tetraedro.
                for v in FCC:
                    vecino = p + v
                    if dentro(vecino):
                        cylinder(
                            pos=q * a,
                            axis=(vecino - q) * a,
                            radius=r_enlace,
                            color=color.gray(0.6),
                        )

# RED CÚBICA CENTRADA EN LAS CARAS FCC (f)

elif red == "f":
    atomos = []
    for i, j, k in product(range(-1, N + 1), repeat=3):
        for b in FCC:
            p = vector(i, j, k) + b
            if dentro(p):
                atomos.append(p)
                sphere(pos=p * a, radius=r_atomo, color=AZUL)

    d_vecinos = 2**0.5 / 2  # distancia a primeros vecinos (en unidades de a)
    for m in range(len(atomos)):
        for n in range(m + 1, len(atomos)):
            if abs((atomos[n] - atomos[m]).mag - d_vecinos) < 1e-3:
                cylinder(
                    pos=atomos[m] * a,
                    axis=(atomos[n] - atomos[m]) * a,
                    radius=r_enlace,
                    color=color.gray(0.6),
                )

# RED HEXAGONAL COMPACTA (h)

elif red == "h":
    c = (8 / 3) ** 0.5 * a
    # Desplaza el prisma para que su centro coincida con el que usa la cámara.
    origen = vector(N / 2 * a, N / 2 * a - N * c / 2, N / 2 * a)

    vertices = [
        vector(a * cos(radians(t)), 0, a * sin(radians(t))) for t in range(0, 360, 60)
    ]
    huecos = [
        vector(a / 3**0.5 * cos(radians(t)), 0, a / 3**0.5 * sin(radians(t)))
        for t in (30, 150, 270)
    ]

    atomos = []
    for capa in range(N + 1):  # capas A en y = 0, c, 2c...
        altura = vector(0, capa * c, 0)
        for p in [vector(0, 0, 0)] + vertices:
            atomos.append(origen + altura + p)
            sphere(pos=atomos[-1], radius=r_atomo, color=AZUL)
    for capa in range(N):  # capas B en y = c/2, 3c/2...
        altura = vector(0, (capa + 0.5) * c, 0)
        for p in huecos:
            atomos.append(origen + altura + p)
            sphere(pos=atomos[-1], radius=r_atomo, color=AMBAR)

    # Enlaces entre primeros vecinos (todos a distancia a con c ideal)
    for m in range(len(atomos)):
        for n in range(m + 1, len(atomos)):
            if abs((atomos[n] - atomos[m]).mag - a) < 1e-3:
                cylinder(
                    pos=atomos[m],
                    axis=atomos[n] - atomos[m],
                    radius=r_enlace,
                    color=color.gray(0.6),
                )

    # Aristas del prisma hexagonal
    for capa in range(N + 1):
        altura = vector(0, capa * c, 0)
        curve(
            pos=[origen + altura + v for v in vertices + vertices[:1]],
            color=color.gray(0.3),
            radius=0.004 * a,
        )
    for v in vertices:
        curve(
            pos=[origen + v, origen + v + vector(0, N * c, 0)],
            color=color.gray(0.3),
            radius=0.004 * a,
        )

# Aristas de las celdas cúbicas (solo para diamante y FCC)
if red in ("d", "f"):
    esquinas = [vector(x, y, z) for x, y, z in product((0, 1), repeat=3)]
    aristas = [
        (m, n)
        for m in range(8)
        for n in range(m + 1, 8)
        if (esquinas[m] - esquinas[n]).mag == 1
    ]  # 12 aristas del cubo

    for i, j, k in product(range(N), repeat=3):
        o = vector(i, j, k)
        for m, n in aristas:
            curve(
                pos=[(o + esquinas[m]) * a, (o + esquinas[n]) * a],
                color=color.gray(0.3),
                radius=0.004 * a,
            )


def movimiento_camara():
    # Cosas de la web para mejor visualizacion de la escena,
    # botones de vista, giro automático, teclado y clic para centrar.

    """Botones de vista, giro automático, teclado y clic para centrar."""
    CENTRO = vector(N / 2, N / 2, N / 2) * a
    VISTA_INICIAL = vector(-1, -0.6, -1.4)  # dirección en la que mira la cámara
    RANGO_INICIAL = 0.9 * N * a  # cuanto menor, más cerca
    PASO = 0.05  # radianes por pulsación de flecha
    girando = False

    scene.autoscale = False  # para que el zoom no se reajuste solo

    def vista(direccion):
        """Recoloca la cámara mirando al centro en la dirección dada."""
        scene.center = CENTRO
        scene.forward = direccion
        scene.range = RANGO_INICIAL

    def girar(angulo, eje):
        nueva = scene.forward.rotate(angle=angulo, axis=eje)
        # evita pasar por encima del polo, donde la vista da la vuelta
        if abs(nueva.norm().dot(scene.up.norm())) < 0.98:
            scene.forward = nueva

    def tecla(evt):
        k = evt.key.lower()
        lateral = scene.forward.cross(scene.up).norm()
        if k == "left":
            girar(PASO, scene.up)
        elif k == "right":
            girar(-PASO, scene.up)
        elif k == "up":
            girar(PASO, lateral)
        elif k == "down":
            girar(-PASO, lateral)
        elif k in ("w", "+"):
            scene.range *= 0.9  # acercar
        elif k in ("s", "-"):
            scene.range /= 0.9  # alejar
        elif k == "r":
            vista(VISTA_INICIAL)

    def clic(evt):
        """Clic sobre un átomo: la cámara pasa a girar alrededor de él."""
        obj = scene.mouse.pick
        if isinstance(obj, sphere):
            scene.center = obj.pos

    def alternar_giro(b):
        nonlocal girando
        girando = not girando
        b.text = "Parar giro" if girando else "Girar"

    scene.bind("keydown", tecla)
    scene.bind("click", clic)
    vista(VISTA_INICIAL)

    scene.append_to_caption("\nVistas:  ")
    button(text="Inicial", bind=lambda b: vista(VISTA_INICIAL))
    button(text="[100]", bind=lambda b: vista(vector(-1, 0, 0)))
    button(text="[110]", bind=lambda b: vista(vector(-1, -1, 0)))
    button(text="[111]", bind=lambda b: vista(vector(-1, -1, -1)))
    scene.append_to_caption("     ")
    button(text="Girar", bind=alternar_giro)

    # Bucle principal: mantiene el programa vivo y hace el giro automático.
    while True:
        rate(60)
        if girando:
            scene.forward = scene.forward.rotate(angle=0.006, axis=scene.up)


movimiento_camara()
