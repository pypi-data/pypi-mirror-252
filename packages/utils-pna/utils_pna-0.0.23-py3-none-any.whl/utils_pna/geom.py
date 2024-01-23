import numpy as np
from numpy import cos, sin
from shapely.geometry import Point
from utils_pna.dist import haversine

def recta(angulo, punto, t):
    x = punto[0] + t*cos(angulo)
    y = punto[1] + t*sin(angulo)
    return (x,y)

def parsear_argumentos(foco1, foco2, punto):
    if isinstance(foco1, tuple):
        foco1 = Point(foco1)

    if isinstance(foco2, tuple):
        foco2 = Point(foco2)

    if isinstance(punto, tuple):
        punto = Point(punto)

    return foco1, foco2, punto

def distancia_elipsoidal(foco1, foco2, punto):
    foco1, foco2, punto = parsear_argumentos(foco1, foco2, punto)
    dist = haversine(punto, foco1) + haversine(punto, foco2)
    return dist

def punto_elipse(p1, p2, l, angulo, tol):
    t_0 = 0
    t_1 = 0
    d=distancia_elipsoidal(p1, p2, recta(angulo,p1,t_1))
    while d <= l:
        t_1 = t_1+1
        d=distancia_elipsoidal(p1, p2, recta(angulo,p1,t_1))

    tc = t_1
    while abs(d-l) >= tol:
        tc=(t_1+t_0)/2
        d = distancia_elipsoidal(p1, p2, recta(angulo,p1,tc))
        if d-l < 0:
            t_0=tc
        else:
            t_1=tc
    return recta(angulo,p1,tc)

def elipse(p1, p2, l=None, tol=0.1):
    d_0 = distancia_elipsoidal(p1, p2, p1)
    if l is None:
        l = 2*d_0

    try:
        assert(l >= d_0)
    except AssertionError:
        raise ValueError(f"l debería ser más grande la distancia entre focos.\nl: {l}\td_focos: {d_0}")

    angulos = np.linspace(0, 2*np.pi, 360)
    elipse = []
    for i in angulos:
        elipse.append(punto_elipse(p1, p2, l, i, tol))

    return elipse