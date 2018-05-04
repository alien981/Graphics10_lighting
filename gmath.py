import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
	q = calculate_ambient(ambient, areflect)
	w = calculate_diffuse(light, dreflect, normal)
	e = calculate_specular(light, sreflect, view, normal)
	return limit_color([q[0]+w[0]+e[0], q[1]+w[1]+e[1], q[2]+w[2]+e[2]])

def calculate_ambient(alight, areflect):
	return [alight[0]*areflect[0], alight[1]*areflect[1], alight[2]*areflect[2]]

def calculate_diffuse(light, dreflect, normal):
	q = dot_product(normalize(light[0]), normalize(normal))
	return [light[1][0]*dreflect[0] *q, light[1][1]*dreflect[1]*q, light[1][2]*dreflect[2]*q]

def calculate_specular(light, sreflect, view, normal):
	n = normalize(normal)
	l = normalize(light[0])
	v = normalize(view)
	q = 2*dot_product(n, l)
	n[0] *= q
	n[0] -= l[0]
	n[1] *= q
	n[1] -= l[1]
	n[2] *= q
	n[2] -= l[2]
	e = math.pow(dot_product(n, v), 16)
	
	return [light[1][0]*sreflect[0]*e, light[1][1]*sreflect[1]*e, light[1][2]*sreflect[2]*e]

def limit_color(color):
	w = [0, 0, 0]
	q = 0
	while q<3:
		if(color[q]<0):
			w[q] = 0
		elif color[q]>255:
			w[q] = 255
		else:
			w[q] = int(color[q])
		q += 1
	return w

#vector functions
def normalize(vector):
	q = math.pow( (math.pow(vector[0], 2) + math.pow(vector[1], 2) + math.pow(vector[2], 2)), .5)
	return [vector[0]/q, vector[1]/q, vector[2]/q]

def dot_product(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
