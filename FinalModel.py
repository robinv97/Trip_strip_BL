# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 13:23:13 2018

@author: robin
"""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
#from FinalRoughFunc import Roughness
#from BaldwinLomax import BL

n = 201;    dx = 0.25                                                          # numerical parameters

u = np.zeros((n, 1))                                                           # initialize u
v = np.zeros((n, 1))                                                          # initialize v
r = np.zeros((n, 1))                                                           # initialize r 

xmax = 301.0;   ymax = 30.0                                                    # domain size

Re = 100.0;     Ue = 1.0;   delta = 1.0                                        # physical properties

nit = round(xmax/dx);   dy = ymax/((n-1).real)                                 # x-grid
Y = np.arange(0, ymax+dy, dy) [np.newaxis]                                     # y-grid not transposed
y = Y.T 

for j in range(0, n):                                                          # set initial profile
    v[j] = 0.0                              
    if y[j] < delta:                                                           # if vertical distance smaller than
        u[j] = y[j]                                                            # BL thickness, u-velocity = y. If
    else:                                                                      # higher, u-velocity=Ue=1.0
        u[j] = 1.0

A = sp.sparse.diags([np.zeros(n-1), np.zeros(n), np.zeros(n-1)], [-1, 0, 1]).toarray() # initialize matrix A

x = np.zeros(5000)                                                             # initialize x
dstar = np.ndarray(5000,)                                                      # initialize dstar
theta = np.ndarray(5000,)                                                      # initialize theta
H = np.ndarray(5000,)                                                          # initialize H


for it in range(0, 2):                                                       # main loop, sweeps x forward
    uml=u                                                                      # store previous u
    for i in range(1, n-1):                                                    # set coefficients in A
        A[i, i-1] = -v[i]*dx/(2.0*dy)-dx/dy**2/Re
        A[i, i] = u[i]+2.0*dx/dy**2/Re
        A[i, i+1] = v[i]*dx/(2.0*dy)-dx/dy**2/Re
        r[i] = (u[i]**2)                                                       # set r

    A[0, 0] = 1.0; r[0] = 0.0                                                  # lower wall BC
    A[n-1, n-1] = 1.0; r[n-1] = Ue                                             # upper wall BC
    
    u = np.linalg.solve(A, r)                                                  # solve matrix system
    
    v[0] = 0.0                                                                 # sweep upwards in y for v
    for g in range(1, n):
        v[g] = v[g-1]-dy/(2.0*dx)*(u[g]-uml[g]+u[g-1]-uml[g-1])

    x[it] = it*dx                                                              # set x-axis for plot
    U = 1.0-u                                                                  # simplify integration function
    V = u*(1.0-u)                                                              # simplify integration function
    dstar = sp.integrate.trapz(U, y, axis=0)                                   # BL displacement thickness
    theta = sp.integrate.trapz(V, y, axis=0)
    Theta = sp.integrate.cumtrapz(V, y, axis=0)                                # BL momentum thickness
    H[it] = dstar/theta                                                        # BL shape factor
    Dstar = sp.integrate.cumtrapz(U, y, axis=0)
    
#    blt = np.ndarray(201,)  
#    for i in range(0, n):
#        blt[i] = 5.0*(np.sqrt((v[i]*x[i])/Ue))                                     # BL thickness according to Blasius
#    
#    plt.plot(x[0: 1201], H[0:1201], 'r', linewidth=2.0)                            # plot shape factor w.r.t. x
#    plt.ylabel('Shape factor')
#    plt.xlabel('Horizontal domain size')
#    plt.title('Shape Factor Along $x$')
#    plt.show()
#    
    plt.plot(u, y, 'SeaGreen', linewidth=2.0, label="Initial")
    plt.legend(loc=2)                                             # plot velocity profile
    plt.ylabel(r'$y$', fontsize=16)
    plt.xlabel(r'$u$', fontsize=16)
    plt.xlim(0, 1.2)
#    plt.title('Laminar Boundary Layer Velocity Profile')
    plt.show()
    print(it)    
#    
#    plt.plot(x[0:201], blt, linewidth=2.0)                                         # plot BL thickenss
#    plt.ylim(0.0, 5.0)
#    plt.xlabel('Horizontal domain size')
#    plt.ylabel('Boundary Layer Thickness')
#    plt.title('Laminar Boundary Layer Thickness')
#    plt.show()
#    
#    print('dstar = ', float(dstar))
#    print('theta = ', float(theta))
#    print('H = ', H[300])
#%%
A = sp.sparse.diags([np.zeros(n-1), np.zeros(n), np.zeros(n-1)], [-1, 0, 1]).toarray() # initialize matrix A

x = np.zeros(5000)                                                             # initialize x
dstar = np.ndarray(5000,)                                                      # initialize dstar
theta = np.ndarray(5000,)                                                      # initialize theta
H = np.ndarray(5000,)                                                          # initialize H
C = Roughness()

for it in range(301, 750):                                                       # main loop, sweeps x forward
    uml=u                                                                      # store previous u
    for i in range(1, n-1):                                                    # set coefficients in A
        A[i, i-1] = -v[i]*dx/(2.0*dy)-dx/dy**2/Re
        A[i, i] = u[i]+2.0*dx/dy**2/Re
        A[i, i+1] = v[i]*dx/(2.0*dy)-dx/dy**2/Re
        r[i] = (u[i]**2)-C[i]                                                       # set r

    A[0, 0] = 1.0; r[0] = 0.0                                                  # lower wall BC
    A[n-1, n-1] = 1.0; r[n-1] = Ue                                             # upper wall BC
    
    u = np.linalg.solve(A, r)                                                  # solve matrix system
    
    v[0] = 0.0                                                                 # sweep upwards in y for v
    for g in range(1, n):
        v[g] = v[g-1]-dy/(2.0*dx)*(u[g]-uml[g]+u[g-1]-uml[g-1])

    x[it] = it*dx                                                              # set x-axis for plot
    U = 1.0-u                                                                  # simplify integration function
    V = u*(1.0-u)                                                              # simplify integration function
    dstar = sp.integrate.trapz(U, y, axis=0)                                   # BL displacement thickness
    theta = sp.integrate.trapz(V, y, axis=0)
    Theta = sp.integrate.cumtrapz(V, y, axis=0)                                # BL momentum thickness
    H[it] = dstar/theta                                                        # BL shape factor
    Dstar = sp.integrate.cumtrapz(U, y, axis=0)
    
#    blt = np.ndarray(201,)  
#    for i in range(0, n):
#        blt[i] = 5.0*(np.sqrt((v[i]*x[i])/Ue))                                     # BL thickness according to Blasius
#    
#    plt.plot(x[0: 1201], H[0:1201], 'r', linewidth=2.0)                            # plot shape factor w.r.t. x
#    plt.ylabel('Shape factor')
#    plt.xlabel('Horizontal domain size')
#    plt.title('Shape Factor Along $x$')
#    plt.show()
#    
#    plt.plot(u, y, 'g', linewidth=2.0)                                             # plot velocity profile
#    plt.ylabel('Vertical domain size')
#    plt.xlabel('Velocity')
#    plt.title('Laminar Boundary Layer Velocity Profile')
#    plt.show()
#    print(it)
#    
#    plt.plot(x[0:201], blt, linewidth=2.0)                                         # plot BL thickenss
#    plt.ylim(0.0, 5.0)
#    plt.xlabel('Horizontal domain size')
#    plt.ylabel('Boundary Layer Thickness')
#    plt.title('Laminar Boundary Layer Thickness')
#    plt.show()
#    
#    print('dstar = ', float(dstar))
#    print('theta = ', float(theta))
#    print('H = ', H[300])

mu_t = BL()

for it in range(751, 1204):                                                       # main loop, sweeps x forward
    uml=u                                                                      # store previous u
    for i in range(1, n-2):                                                    # set coefficients in A
        A[i, i-1] = -v[i]*dx/(2.0*dy)-(((1/Re)+mu_t[i])*(dx/dy**2))-((dx/(4*dy**2))*(mu_t[i-1]-mu_t[i+1]))
        A[i, i] = u[i]+((2.0*dx/dy**2)*((1/Re)+mu_t[i]))
        A[i, i+1] = v[i]*dx/(2.0*dy)-(((1/Re)+mu_t[i])*(dx/dy**2))-((dx/(4*dy**2))*(mu_t[i+1]-mu_t[i-1]))
        r[i] = (u[i]**2)                                                       # set r

    A[0, 0] = 1.0; r[0] = 0.0                                                  # lower wall BC
    A[n-1, n-1] = 1.0; r[n-1] = Ue                                             # upper wall BC
    
    u = np.linalg.solve(A, r)                                                  # solve matrix system
    
    v[0] = 0.0                                                                 # sweep upwards in y for v
    for g in range(1, 201):
        v[g] = v[g-1]-dy/(2.0*dx)*(u[g]-uml[g]+u[g-1]-uml[g-1])

    x[it] = it*dx                                                              # set x-axis for plot
    U = 1.0-u                                                                  # simplify integration function
    V = u*(1.0-u)                                                              # simplify integration function
    dstar = sp.integrate.trapz(U, y, axis=0)                                   # BL displacement thickness
    theta = sp.integrate.trapz(V, y, axis=0)
    Theta = sp.integrate.cumtrapz(V, y, axis=0)                                # BL momentum thickness
    H[it] = dstar/theta                                                        # BL shape factor
    Dstar = sp.integrate.cumtrapz(U, y, axis=0)
    
#blt = np.ndarray(201,)  
#for i in range(0, n):
#    blt[i] = 5.0*(np.sqrt((v[i]*x[i])/Ue))                                     # BL thickness according to Blasius
#
#plt.plot(x[0: 299], H[0:299], 'r', linewidth=2.0)                            # plot shape factor w.r.t. x
#plt.ylabel('Shape factor')
#plt.xlabel('Horizontal domain size')
#plt.title('Shape Factor Along $x$')
#plt.show()
#
    plt.plot(u, y, 'g', linewidth=2.0)                                             # plot velocity profile
    plt.ylabel('Vertical domain size')
    plt.xlabel('Velocity')
    plt.title('Laminar Boundary Layer Velocity Profile')
    plt.show()
    print(it)
#
#plt.plot(x[0:201], blt, linewidth=2.0)                                         # plot BL thickenss
#plt.ylim(0.0, 5.0)
#plt.xlabel('Horizontal domain size')
#plt.ylabel('Boundary Layer Thickness')
#plt.title('Laminar Boundary Layer Thickness')
#plt.show()
#
#print('dstar = ', float(dstar))
#print('theta = ', float(theta))
#print('H = ', H[299])