import math
import matplotlib.pyplot as plt
import scipy.integrate as i

t = 0

xpos = 0
ypos = 0

initialvelocity = 60
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

# test för del 1 i steg 2
# print(f"x-positions = {x_positions} \n y-positions = {y_positions}")

def ballstopp(t, u):
    xpos, ypos, xspeed, yspeed = u
    # Returnerar 0 när xspeed är 0.01. Då triggas eventet.
    return xspeed - 0.01 

ballstopp.terminal = True  # Avbryt simuleringen när detta händer
ballstopp.direction = -1   # Triggas när hastigheten minskar och passerar värdet

plt.figure()
plt.plot(x_positions, y_positions)
plt.title('Golfbollens bana')
plt.xlabel('Horisontellt avstånd (m)')
plt.ylabel('Vertikal höjd (m)')
plt.grid(True)
plt.savefig("steg2-graf.png")
plt.show()
print(x_positions[-1])