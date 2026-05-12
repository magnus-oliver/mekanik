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
    # Parametrar för hålet enligt instruktionerna
    vhalmax = 0.2  # [cite: 66]
    windspeed = -5 # Motvind 
    
    # Vi testar ett intervall av hastigheter och vinklar
    for velocity_test in range(40, 70): # Testa hastighet mellan 40-70 m/s
        for angle_test in range(10, 45): # Testa vinkel mellan 10-45 grader
            
            test_rad = math.radians(angle_test)
            v0_x = math.cos(test_rad) * velocity_test
            v0_y = math.sin(test_rad) * velocity_test
            u_test = [0, 0, v0_x, v0_y]

            # Kör simuleringen
            sol = i.solve_ivp(
                fun=forcecalc,
                t_span=[0, 20],
                y0=u_test,
                events=ballstop, # Din befintliga event-funktion som stoppar vid vx ~ 0
                max_step=0.1
            )

            # Kontrollera slutposition och sluthastighet
            final_x = sol.y[0][-1]
            final_vx = sol.y[2][-1]

            # Om vi är nära hålet (190m) och bollen rullar tillräckligt sakta
            if abs(final_x - xhal) < 0.5 and final_vx < vhalmax:
                print("--- HOLE IN ONE HITTAD! ---")
                print(f"Utgångshastighet: {velocity_test} m/s")
                print(f"Vinkel: {angle_test} grader")
                print(f"Slutposition: {final_x:.2f} m")
                print(f"Sluthastighet: {final_vx:.3f} m/s")
                return velocity_test, angle_test, sol # Returnerar lösningen för plottning

    print("Hittade ingen hole-in-one med nuvarande intervall.")
    return None

# Kör sökningen och plotta resultatet
result = find_hole_in_one()
if result:
    v0_opt, angle_opt, hole_sol = result
    plt.figure()
    plt.plot(hole_sol.y[0], hole_sol.y[1], 'g-', label='Hole-in-one bana')
    plt.plot(xhal, 0, 'x', 'ro', label='Hålet (190m)', color='green')
    plt.title(f'Hole-in-one: {v0_opt}m/s vid {angle_opt} grader')
    plt.xlabel('Horisontellt avstånd (m)')
    plt.ylabel('Vertikal höjd (m)')
    plt.legend()
    plt.grid(True)
    plt.savefig("steg4-graf.png")
    plt.show()