from numpy import array, round, zeros
from numpy.linalg import eig, inv

# Repaso de arrays en python y algunas cosillas
# basicas

lista = [1, 2, 3, 4, 5]
print(lista)

x = 5
y = 10
z = 1

r = [x, y, z]
print(r)

r.append(15)  # r.pop elimina el ultimo elemento
print("r = ", r)
Valores = [max(r), min(r), sum(r), len(r)]

print(Valores, "\n")

# tablas
a = zeros((3, 4))
print(a, "\n")

print(
    "Matriz bonita para diagonalizar: \n",
    array([[1, 1, -1], [0, 2, 1], [0, 0, 3]]),
    "\n",
)

# Peticion al usuario de una matriz cuadrada para diagonalizarla

lenght = int(input("Introduce el tamaño de la matriz cuadrada: "))

if lenght > 0:
    matriz = zeros((lenght, lenght))
    for i in range(lenght):
        datos = input("Introduce numeros separados por espacios: ")
        matriz[i] = [float(v) for v in datos.split()]
    print("Matriz introducida: \n", matriz, "\n")


# Diagonalizacion de la matriz introducida
autovalores, autovectores = eig(matriz)

# Les quito la parte imaginaria a los autovalores
# y autovectores para verlos mejor en pantalla

autovalores = autovalores.real
autovectores = autovectores.real
print("Autovalores: ", autovalores, "\n")
print("P: \n", autovectores, "\n")

p_inv = inv(autovectores)
D = round(p_inv @ matriz @ autovectores, 2)
print("p*A*P^-1 = \n", D, "\n")
