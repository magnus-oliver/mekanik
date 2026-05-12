import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as i

g = -9.81
ballmass = 46e-3
windspeed = 0  
airdensity = 1.225
dragkoefficient = 0.25
area = 1430e-6
k = 1000
c = 2
my = 0.15
initialvelocity = 50

def forcecalc(t, u):
    xpos, ypos, xspeed, yspeed = u
    if ypos > 0:
        vrelx = xspeed - windspeed
        vrely = yspeed
        vrel = math.sqrt(vrelx**2 + vrely**2)
        df = 0.5 * airdensity * dragkoefficient * area * vrel**2 # [cite: 45]
        
        forcex = -df * vrelx / vrel # [cite: 47]
        forcey = -df * vrely / vrel
        accx = forcex / ballmass
        accy = forcey / ballmass + g
    else:
        forcex = -my * ballmass * abs(g) * xspeed
        accx = forcex / ballmass
        forcey = k * (-ypos) + c * (-yspeed)
        accy = forcey / ballmass + g
    return [xspeed, yspeed, accx, accy]

def ballstop(t, u):
    return u[2] - 0.01 
ballstop.terminal = True
ballstop.direction = -1

def optimalangle():
    best_dist = 0
    best_sol = None
    best_angle = 0
    
    for n in range(0, 181):
        angle = n / 2 
        anglerad = math.radians(angle)
        u0 = [0, 0, math.cos(anglerad)*initialvelocity, math.sin(anglerad)*initialvelocity]

        sol = i.solve_ivp(
            fun=forcecalc,
            t_span=[0, 25],
            y0=u0,
            events=ballstop,
            max_step=0.1
        )
        
        final_x = sol.y[0][-1]
        if final_x > best_dist:
            best_dist = final_x
            best_sol = sol
            best_angle = angle
    
    print(f"Längsta slaget: {best_dist:.2f} m vid vinkeln {best_angle} grader")
    return best_sol, best_angle

best_sol, best_angle = optimalangle()

if best_sol:
    x_vals = best_sol.y[0]
    y_vals = best_sol.y[1]
    vx_vals = best_sol.y[2]
    vy_vals = best_sol.y[3]



    plt.figure(figsize=(10, 4))
    plt.plot(x_vals, y_vals, label=f'Bästa slag ({best_angle}°)')
    final_dist = best_sol.y[0][-1]

    plt.text(0.05,0.05, f"Maximal räckvidd: {final_dist:.2f} m", 
        transform=plt.gca().transAxes,
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    plt.title(f'Golfbollens bana - Optimal vinkel: {best_angle}°')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.legend()
    plt.grid(True)
    plt.savefig("steg3-graf.png")
    
    plt.show()