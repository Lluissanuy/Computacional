'''
Sobresimplificación del problema

El estado físico de un sistema unidimensional en mecánica cuántica viene definido por
una función de onda (phi) que debe obedecer la ecuación de Schrodinger en la que se
incluye un potencial al que está sometida la partícula y un hamiltoniano. 

En este programa se plantea resolver esta ecuación y calcular la densidad de probabilidad 
de encontrar a la partícula en un punto del espacio conforme avanza el tiempo usando, 
de manera predefinida un potencial escalón y una función de onda inicial de una onda
plana, aunque estas dos funciones pueden modificarse sencillamente según las necesidades
del usuario.

Se trata de una ecuación diferencial en la que se va a discretizar el tiempo y el espacio. 

Resolución numérica de la ecuación de Schrodinger:

Discretizar el espacio dando el número total de puntos (n_particulas)
Discretizar el tiempo dando el número total de iteraciones que se quieren hacer (iteraciones)
Implementar salto temporal (s)

A partir de una función de onda inicial se calculará la función de onda de la siguiente
iteración usando una función auxiliar chi (chi)

phi(t+1) = chi(t) - phi(t)

Condiciones de contorno -> tanto phi como chi son 0 en inicio y fin.

En cada instante de tiempo:

chi(posicion j) = alpha(posicion j-1) * chi(posicion j-1) +beta(posicion j-1)

alpha y beta son coeficientes auxialiares que son necesarios y que se calculan en el program
pero su obtención es muy compleja para detallarla.

Función de onda inicial -> onda plana con amplitud gausiana.
	
	phi(x,0) = e^(ik0x)e^[(x-x0)^2/(2*sigma)^2]

	k0 = 2*pi*n_ciclos/(Nh) -> variable a tomar (n_ciclos = 1, ..., N/4 tendrá 4 puntos como mínimo)

	x_0 = Nh/4
	sigma = Nh/16

Potencial escalón de anchura N/5, centrado en N/2 y altura proporcional a la función de onda incidente 
	altura = lambda*k0^2  (lambda = 0.3)	
'''


import numpy as np 
import cmath
import matplotlib.pyplot as plt
from matplotlib import animation

def potencial(centro, anchura):
	'''
	Potencial escalón que toma la altura -> cte_lambda * k_0**2 

	cte_lambda sirve para modificar SOLAMENTE la altura del potencial
	k_0 se calcula a partir de n_ciclos, también sirve para modificar la altura pero afecta a otras cosas.
	'''
	
	lim_inf = centro - anchura/2
	lim_sup = lim_inf + anchura
	
	cte_lambda = 0.3		#Término para la altura del potencial

	potencial = np.array([cte_lambda * k_0**2 if lim_inf <= j < lim_sup else 0 for j in range(n_particulas)])

	return potencial

def funcion_inicial(pos_inicial, anchura_inicial):
	#Expresión de una función de onda gaussiana
	phi = np.array([cmath.exp(1j*k_0*i) * cmath.exp(-1 * (i - pos_inicial)**2/(2 * anchura_inicial**2)) for i in range(n_particulas)])
	
	phi[0] = 0 + 0j
	phi[n_particulas-1] = 0 + 0j

	return phi


def pedir_entero(peticion):
	while True:
		try:
			numero = int(input(peticion))
		
		except:
			print("Introduzca un número.\n")

		else:
			if numero < 0:
				print("Introduzca un número mayor a 0.\n")
			else:
				break
	
	return numero
	
#Variables principales


n_particulas = pedir_entero("Introduzca el número de partículas: ")
iteraciones = pedir_entero("Introduzca el número de iteraciones: ")

n_ciclos = n_particulas/6

#Frecuencia de oscilación
k_0 = 2 * np.pi * n_ciclos/n_particulas

#Salto temporal
s = 1/(4*k_0**2)

#cálculo del potencial
centro_potencial = n_particulas/2
anchura_potencial = n_particulas/5
potencial = potencial(centro_potencial, anchura_potencial)

#Función de onda inicial
centro_funcion = n_particulas/4
anchura_funcion = n_particulas/16
phi = funcion_inicial(centro_funcion, anchura_funcion)

x = np.array([i for i in range(n_particulas)])

plt.plot(x, abs(phi),  x, potencial, "b", "r", lw=2)
plt.title("Función de onda inicial")
plt.xlabel("x")
plt.ylabel("|phi|")
plt.show()


#Constantes A para el cálculo de los coeficientes alpha
a_minus = np.array([1 + 0j for i in range(n_particulas)])
a_0 = np.array([-2+2j/s -potencial[i] for i in range(n_particulas)])
a_plus = np.array([1 + 0j for i in range(n_particulas)])

alpha = np.array([0 + 0j for i in range(n_particulas)]) 

#Recurrencia inversa para calcular el valor de los coeficientes alpha
for i in range(n_particulas-3, -1, -1):
	'''
	Para calcular los coeficientes alpha tengo que hacer una división por un 
	número complejo. Como esto no está implementado en python, hasta encontrar
	una forma distinta de hacerlo, voy a calcularlo más manualmente.
	Primero calculo el denominador, que será el número complejo
	A la hora de hacer la división multiplico por el conjugado y divido por 
	la suma del cuadrado de la parte real más el cuadrado de la parte imaginaria.
	'''

	denominador = a_0[i + 1] + a_plus[i + 1] * alpha [i + 1]
	division_compleja = denominador.conjugate()/(denominador.real **2 + denominador.imag**2)
	
	alpha[i] = -a_minus[i + 1] * division_compleja


#Valores iniciales de los valores recurrentes
beta = np.array([0 + 0j for i in range(n_particulas)])
chi = np.array([0 + 0j for i in range(n_particulas)])

lista_funciones = []

for iteracion in range(iteraciones):
	#calculo los coeficientes beta
	for i in range(n_particulas - 3, -1, -1):

		denominador = a_0[i + 1] + a_plus[i + 1] * alpha[i + 1]
		division_compleja = denominador.conjugate()/(denominador.real**2 + denominador.imag**2)

		coeficientes_b = 4j*phi/s
		beta[i] = division_compleja * (coeficientes_b[i + 1] - a_plus[i + 1] * beta[i + 1])
	

	for i in range(1, n_particulas):
		chi[i] = alpha[i - 1] * chi[i - 1] + beta[i - 1]

	lista_funciones.append(abs(phi))
	
	phi = chi - phi

#Creación de la animación
fig = plt.figure()
ax = plt.axes(xlim=(0, n_particulas), ylim=(-1, 2))
line, = ax.plot([], [], lw=2)
line2, = ax.plot([], [], lw=2)

def init():
	line.set_data([], [])
	line2.set_data([], [])
	return line, line2

def animate(frame):
	x = np.array([i for i in range(n_particulas)])
	y = lista_funciones[frame]

	line.set_data(x, y)
	line2.set_data(x, potencial)
	return line, line2


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=iteraciones, interval=20, blit=True)
plt.show()


np.savetxt("distr_probab.csv", lista_funciones, delimiter=",")
'''
for paso in lista_funciones:
	print(type(paso))
	print(len(paso))
	np.savetxt("distr_probab.csv", paso, delimiter=",")


'''