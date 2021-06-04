'''
El método de ising trata de mostrar cómo, a partir de una cierta temperatura, 
un sistema inicial aparentemente caótico se ordena tendiendo hacia uno de sus dos
estados posibles.

Se parte de una matriz inicial N x N cuyos elementos pueden tomar dos estados
(+ 1 o -1) y utilizando un criterio de selección basado en la temperatura del 
sistema, se observa cómo se modifican los elementos de la matriz. 

En este caso hacemos correspondencia con un sistema magnético en el que la matriz
representa un material paramagnético (no magnético) en el que los elemento simulan
el espín de los electrones (+1 espín arriba, -1 espín abajo) Si se introduce una 
temperatura superior a 2 kelvin aproximadamente se observa como el sistema permanece
en un estado caótico mientras que si se baja esta temperatura se observa claramente 
una tendencia a uno de los dos estados posibles. 

La simulación se realiza usando pasos de montecarlo en el que cada paso se tratan de 
modificar NxN elementos y, calculando la energía de cada elemento usando sus vecinos
cercanos. Si la exponencial de esta energía dividida por la temperatura es menor que 
un número aleatorio elegido entre 0 y 1, el elemento cambiará su valor, en caso 
contrario no lo hará.

'''

import random
import matplotlib.pyplot as plt
from math import exp
from matplotlib import animation


def pedir_entero(peticion):
	while True:
		try:
			numero = int(input(peticion))

		except:
			print("Introduzca un número.\n")

		else:
			if numero <= 0:
				print("Introduzca un número mayor a 0.\n")
			else:
				break

	return numero

def pedir_float(peticion):
	while True:
		try:
			numero = float(input(peticion))

		except:
			print("Introduzca un número.\n")

		else:
			if numero <= 0:
				print("Introduzca un número mayor a 0.\n")
			else:
				break

	return numero


N = pedir_entero("Introduzca la dimensión de la matriz (cuadrada): ")
temp= pedir_float("Introduzca la temperatura: ")
iteraciones = pedir_entero("Introduzca el número de iteraciones: ")

salto_iteraciones = pedir_entero("Introduzca cada cuantas iteraciones quiere ver el sistema: ")

lista = [[0 for i in range(N)] for j in range(N)]

#Modificar la semilla si se quiere repetir la malla inicial
#random.seed(5)

for i in range(N):
	for j in range(N):
		selector = random.random()
		
		if selector <= 0.5:
			lista[i][j] = -1

		else:
			lista[i][j] = 1


plt.imshow(lista)
plt.show()

registro_listas = []
def animacion(i):		
	#paso de montecarlo
	for j in range(N * N):
		x = random.randrange(0,N)
		y = random.randrange(0,N)
	
		if x == 0:
			vec_izq = lista[N - 1][y]
			vec_der = lista[x + 1][y]

		elif x == N - 1:
			vec_izq = lista[x - 1][y]
			vec_der = lista[0][y]

		else: 
			vec_izq = lista[x - 1][y]
			vec_der = lista[x + 1][y]
		
		if y == 0:
			vec_arr = lista[x][N - 1]
			vec_abj = lista[x][y + 1]

		elif y == N - 1:
			vec_arr = lista[x][y - 1]
			vec_abj = lista[x][0]

		else: 
			vec_arr = lista[x][y - 1]
			vec_abj = lista[x][y + 1]

		energia = 2 * lista[x][y] * (vec_der + vec_abj + vec_arr + vec_izq)
		p = min(1, exp(-energia/temp))
		comparador = random.uniform(0,1)
	
		if comparador < p:
			lista[x][y] *= -1
	
	if i % salto_iteraciones == 0:
		plt.imshow(lista)
		plt.title("iteracion = {}".format(i))
		plt.show()


fig = plt.figure()

def init():
	plt.clf()
	
anim = animation.FuncAnimation(fig, animacion, init_func = init, frames = iteraciones, interval = 20)
plt.show()
'''

ax_va = add_axes_inches(fig, [cellsize, cellsize, axwidth, axheight])
im_va = ax_va.imshow(va_color, vmin=0., vmax=1.3, cmap="Blues")
im_va.set_array(c)
'''
