## Loops through updating graphs 

import urwid as urwid
import json
import comm
import box
import time

palette = [
    ('normal', 'dark magenta', 'dark gray'),
    ('inverse', 'dark gray', 'dark magenta'),
]

def init():
    comm.init()
    global data
    data = {'time': -1, 'state': 'no_comm', 'sensors': None}
    global accelArray
    accelArray = []
    global altArray
    altArray = []

def update():
    global accelArray
    global altArray
    try:
        cmd = sys.stdin.read(1)
        comm.send(cmd)
    except IOError:
        pass

    message = comm.read()

    if message:
        data['time'] = message['time']

        if message['type'] == 'state':
            data['state'] = message['state']
        elif message['type'] == 'telemetry':
            data['sensors'] = message['sensors']

    if data['sensors']:
        accelArray.append(states['sensors']['acc']['z'])
        altArray.append(states['sensors']['bar']['alt'])

def updatefake(loop, data):
    print(data)
    time.sleep(2)
    newData = [(1,),(3,),(9,),(4,),(0,),(0,),(15,)]
    lines = [50]
    #data.set_data(newData, 50, lines)
    loop.draw_screen()
    time.sleep(0.5)
    newData = [(5,),(2,),(3,),(4,),(0,),(3,),(0,)]
    loop.draw_screen()
    time.sleep(0.5)
    #updatefake(loop,data)
        
##Just altitude graph for now
def graph():
    altitudeGraph = urwid.BarGraph(
        ['normal', 'inverse'],
        ['normal', 'inverse'],
        { (1,0): 'normal', },
    )
    global altArray
    lines = [50]
    altitudeGraph.set_data(altArray, 50, lines)
    loop = urwid.MainLoop(altitudeGraph, palette)
    loop.set_alarm_in(2,updatefake)
    loop.run()

altArray = [(1,),(2,),(3,),(4,),(0,),(3,),(6,)] #temp until fake data parse
altitudeGraph = urwid.BarGraph(
    ['normal', 'inverse'],
    ['normal', 'inverse'],
    { (1,0): 'normal', },
)

def updateGraph():
    altitudeGraph.set_data(altArray, 50)
    altArray = [(1,),(2,),(3,),(4,),(0,),(3,),(6,)]
    altitudeGraph.set_data(altArray, 50)
    altArray = [(5,),(4,),(5,),(4,),(0,),(6,),(3,)]

loop = urwid.MainLoop(updateGraph, palette)
loop.run()

#init()
'''while(True):
    #update()
    graph()
    #time.sleep(3)
    #print("swag")
    #time.sleep(3)
    altArray = [(3,),(2,),(0,),(0,),(0,),(6,),(1,)]
    graph()'''
