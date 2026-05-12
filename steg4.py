import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as i

t = 0

xpos = 0
ypos = 0

initialvelocity = 50
angle = 15

xspeed = 0
yspeed = 0

g = -9.81
timeinair = 0
ballmass = 46e-3
gforce = ballmass*g
windspeed = -5
airdensity = 1.225
dragkoefficient = 0.25
area = 1430e-6

k = 1000
c = 2
my = 0.15

xhal = 190

anglerad = math.radians(angle)
xspeed = math.cos(anglerad)*initialvelocity
yspeed = math.sin(anglerad)*initialvelocity

u0 = [0, 0, xspeed, yspeed]
u = [xpos, ypos, xspeed, yspeed]

def balltrajectory():
    x, y, xspeed, yspeed = u
    
    xpos = ((initialvelocity**2)*math.sin(2*anglerad))/-g
    timeinair = xpos/xspeed
    return u

balltrajectory()

def forcecalc(t, u):
    xpos, ypos, xspeed, yspeed = u

    if ypos > 0:
        vrelx = xspeed - windspeed
        vrely = yspeed
        vrel = math.sqrt(vrelx**2+vrely**2)

        df = airdensity * dragkoefficient * area * abs(vrel)**2 * 1/2

        forcex = -df*vrelx/vrel
        forcey = -df*vrely/vrel

        accx = forcex/ballmass
        accy = forcey/ballmass + g
    
    else:
        forcex = -my * ballmass * abs(g) * xspeed
        accx = forcex/ballmass

        forcey = k * (-ypos) + c * (-yspeed)
        accy = forcey / ballmass + g

    return [xspeed, yspeed, accx, accy]

solution = i.solve_ivp(
    fun=forcecalc,
    t_span = [0,20],
    y0=u0,
    max_step=0.1
)

x_positions = solution.y[0]
y_positions = solution.y[1]

def ballstop(t, u):
    xpos, ypos, xspeed, yspeed = u
    # Returnerar 0 när xspeed är 0.01. Då triggas eventet.
    return xspeed - 0.01 

ballstop.terminal = True  # Avbryt simuleringen när detta händer
ballstop.direction = -1   # Triggas när hastigheten minskar och passerar värdet

anglelist = []

def optimalangle():
    for n in range(0,180):
        angle = n / 2 
        
        anglerad = math.radians(angle)
        start_xspeed = math.cos(anglerad) * initialvelocity
        start_yspeed = math.sin(anglerad) * initialvelocity

        current_u0 = [0, 0, start_xspeed, start_yspeed]

        solution = i.solve_ivp(
            fun=forcecalc,
            t_span=[0, 20],
            y0=current_u0,
            events=ballstop,
            max_step=0.1
        )

        x_positions = solution.y[0]
        final_x = x_positions[-1]

        anglelist.append([final_x, angle])
    
    best_result = max(anglelist)
    
    print(f"Längsta slaget: {best_result[0]:.2f} m vid vinkeln {best_result[1]} grader")


def find_hole_in_one():
    vhalmax = 0.2
    for velocity_test in range(40, 75): 
        for angle_test in range(10, 45):
            test_rad = math.radians(angle_test)
            v0_x = math.cos(test_rad) * velocity_test
            v0_y = math.sin(test_rad) * velocity_test
            u_test = [0, 0, v0_x, v0_y]

            sol = i.solve_ivp(
                fun=forcecalc,
                t_span=[0, 20],
                y0=u_test,
                events=ballstop,
                max_step=0.1
            )

            final_x = sol.y[0][-1]
            final_vx = sol.y[2][-1]

            if abs(final_x - xhal) < 0.02 and final_vx < vhalmax:
                return {
                    'velocity': velocity_test,
                    'angle': angle_test,
                    'pos': final_x,
                    'speed': final_vx,
                    'sol': sol
                }
    return None

result = find_hole_in_one()

if result:
    res_sol = result['sol']
    
    plt.figure(figsize=(10, 6))
    plt.plot(res_sol.y[0], res_sol.y[1], 'b-', label='Hole-in-one bana')
    plt.plot(xhal, 0, 'gx', markersize=10, label='Hålet (190m)') # Grön cirkel för hålet
    
    info_text = (
        f"--- Resultat ---\n"
        f"Utslagshastighet: {result['velocity']} m/s\n"
        f"Utslagsvinkel: {result['angle']}°\n"
        f"Slutposition: {result['pos']:.2f} m\n"
        f"Sluthastighet: {result['speed']:.3f} m/s"
    )
    
    plt.text(0.05, 0.95, info_text, transform=plt.gca().transAxes, 
             fontsize=10, verticalalignment='top', 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.title(f"Hole-in-one på {xhal}m (med {abs(windspeed)}m/s motvind)")
    plt.xlabel('Horisontellt avstånd (m)')
    plt.ylabel('Vertikal höjd (m)')
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig("steg4-graf.png")
    plt.show()
else:
    print("Ingen lösning hittades. Prova att öka intervallet för velocity_test.")