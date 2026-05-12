import math
import numpy as np
import matplotlib.pyplot as plt

xpos = 0
ypos = 0

initialvelocity = 50
angle = 15

xspeed = 0
yspeed = 0

g = -9.82
timeinair = 0

def balltrajectory():

    anglerad = math.radians(angle)
    
    xspeed = math.cos(anglerad)*initialvelocity
    yspeed = math.sin(anglerad)*initialvelocity

    if ypos < 0: # ta bort senare
        xspeed = 0
        yspeed = 0
    
    xpos = ((initialvelocity**2)*math.sin(2*anglerad))/-g
    timeinair = xpos/xspeed

    print(f"xspeed: {xspeed}, yspeed: {yspeed}, xpos: {xpos}, timeinair: {timeinair}")
    return timeinair, xspeed, yspeed

# Hämta data för simuleringen
time_limit, vx, vy = balltrajectory()

t_values = np.linspace(0, time_limit, 100)

x_points = vx * t_values
y_points = vy * t_values + 0.5 * g * t_values**2

# --- Plotta grafen ---
plt.figure(figsize=(10, 5))
plt.plot(x_points, y_points, linestyle='--', label=f"Vinkel: {angle}°", color="blue")

# Formatering av grafen
plt.title("Bollens bana (Kastparabel)")
plt.xlabel("Avstånd (m)")
plt.ylabel("Höjd (m)")
plt.grid(True, linestyle='--', alpha=0.7)
plt.axhline(0, color='black', linewidth=1) # Markera marknivå
plt.legend()

# Spara grafen
plt.savefig("steg1-graf.png")

# Visa grafen (valfritt)
plt.show()

print("Grafen har sparats som 'steg1-graf.png'")