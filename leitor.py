#!/usr/bin/python
import sys
import serial
import struct
import time
import math

BITS = 5
div = (1<<BITS)

s = serial.Serial(sys.argv[1], 57600)

def ler_dados():
    while True:
        xyz = s.readline()
        xyz = xyz.split('\t')
        try:
            xyz[2] = xyz[2].strip()
            xyz = [float(xyz[0])/div, float(xyz[1])/div, float(xyz[2])/div]
        except (IndexError, ValueError):
            continue
        break
    return xyz

gravidade = [0., 0., 0.]
pos  = [0., 0., 0.]
pos0 = [0., 0., 0.]
vel  = [0., 0., 0.]
vel0 = [0., 0., 0.]
acc  = [0., 0., 0.]
acc0 = [0., 0., 0.]
def reset():
    global gravidade
    global pos
    global pos0
    global vel
    global vel0
    global acc
    global acc0
    gravidade = ler_dados()
    pos  = [0., 0., 0.]
    pos0 = [0., 0., 0.]
    vel  = [0., 0., 0.]
    vel0 = [0., 0., 0.]
    acc  = [0., 0., 0.]
    acc0 = [0., 0., 0.]

print "Esperando"
time.sleep(0.2)
print "Pronto"
ler_dados()
reset()
print "Gravidade"
print gravidade

dt = div/2000.
movimento0 = False

while True:
    leitura = ler_dados()
    pos0 = pos
    vel0 = vel
    acc0 = acc

    for i in range(0, 3):
        acc[i] = leitura[i] - gravidade[i]

# comeco deteccao de movimento
    movimento = acc[0] >= 3. or acc[0] <= -3. or acc[1] >= 3. or acc[1] <= -3. or acc[2] >= 3. or acc[2] <= -3.

    for i in range(0, 3):
        acc[i] = (acc[i] / 248.) * 9.81

    if not movimento0:
        movimento0 = movimento
        if movimento0:
            print "movimento comecou"
    if movimento0:
        if movimento:
            sem_movimento = 0
# comeco das contas
            for i in range(0, 3):
                vel[i] = vel0[i] + dt*(acc[i] + acc0[i])/2.
                pos[i] = pos0[i] + dt*(vel[i] + vel0[i])/2.
#            print pos
            print math.sqrt(pos[0]*pos[0]+pos[1]*pos[1]+pos[2]*pos[2])
# fim das contas
        else:
            sem_movimento += 1
        if sem_movimento is 10:
            movimento0 = False
            reset()
            print "movimento acabou"
# fim deteccao de movimento

    leitura0 = leitura
