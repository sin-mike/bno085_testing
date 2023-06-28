from vpython import *
from time import *
import numpy as np
import math
import serial

scene.range=5
toRad=2*np.pi/360
toDeg=1/toRad
scene.forward=vector(-1,-1,-1)

scene.width=600
scene.height=600

xarrow=arrow(lenght=2, shaftwidth=.1, color=color.red,axis=vector(1,0,0))
yarrow=arrow(lenght=2, shaftwidth=.1, color=color.green,axis=vector(0,1,0))
zarrow=arrow(lenght=4, shaftwidth=.1, color=color.blue,axis=vector(0,0,1))

# frontArrow=arrow(length=4,shaftwidth=.1,color=color.purple,axis=vector(0,1,0))
# upArrow=arrow(length=1,shaftwidth=.1,color=color.magenta,axis=vector(0,1,0))
sideArrow=arrow(length=2,shaftwidth=.1,color=color.orange,axis=vector(0,0,1))

bBoard=box(length=2,width=6,height=.2,opacity=.8,pos=vector(0,0,0,))
myObj=compound([bBoard])

ad=serial.Serial('/dev/cu.usbserial-0001', 115200)
ad.readline()
ad.readline()
ad.readline()

toRad=2*np.pi/360
toDeg=1/toRad

while (True):

    try:
        while (ad.in_waiting>300):
            ad.readline()
        splitPacket=ad.readline()[:-2].decode().split('\t')
        
        roll=float(splitPacket[0])*toRad
        pitch=float(splitPacket[1])*toRad
        yaw=float(splitPacket[2])*toRad#+np.pi
        
        print(f"Roll={roll*toDeg:.3f} Pitch={pitch*toDeg:.3f} Yaw={yaw*toDeg: .3f}", end='      \r')
    except Exception as e:
        print(e)
    rate(50)
    k=-vector(cos(yaw)*cos(pitch), sin(pitch),sin(yaw)*cos(pitch))
    y=vector(0,1,0)
    s=cross(k,y)
    v=cross(s,k)
    vrot=v*cos(roll)+cross(k,v)*sin(roll)

    # frontArrow.axis=k
    sideArrow.axis=cross(k,vrot)
    # upArrow.axis=vrot
    myObj.axis=k
    myObj.up=vrot
    sideArrow.length=2
    # frontArrow.length=4
    # upArrow.length=1