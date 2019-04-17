import krpc
import time
from os import system
def main():
    conn = krpc.connect()
    planes = []
    commandQueue = []
    game = gameLoop(conn,commandQueue)
    for i in range(100):
        game.update()
        time.sleep(2)

class Plane:
    def __init__(self,starthp,startfuel,startammo,hp,fuel,ammo,name,i,team):
        self.id = str(i)
        self.name = name
        self.StartHp = starthp+0.001
        self.StartFuel = startfuel+0.001
        self.StartAmmo = startammo+0.001
        self.Hp = hp
        self.Fuel = fuel
        self.Ammo = ammo
        self.team = team

class gameLoop:
    def getHp(self,vessel):
        sum = 0
        for part in vessel.parts.all:
            for module in part.modules:
                if module.name == "HitpointTracker":
                    sum += float(module.get_field('Hitpoints')[:6])
        return sum
    def __init__(self,conn,commandQueue):
        self.commandQueue = commandQueue
        self.conn = conn
        self.planes = []
        self.InitialPlanes = []
        i = 0
        for vessel in conn.space_center.vessels:
            if vessel.parts.with_module("ModuleCommand") and vessel.parts.with_module("MissileFire"):
                #print(vessel.name)
                hp = self.getHp(vessel)
                resources = vessel.resources
                #print(resources.names)
                fuel = 0
                mm20 =0
                mm30 =0
                cal50=0
                team = vessel.parts.modules_with_name("MissileFire")
                #print(team[0].fields)
                team = team[0].get_field('Team')
                if resources.has_resource("LiquidFuel"):
                    fuel = resources.amount("LiquidFuel")
                if resources.has_resource("20x102Ammo"):
                    mm20 = resources.amount("20x102Ammo")
                if resources.has_resource("30x173Ammo"):
                    mm30 = resources.amount("30x173Ammo")
                if resources.has_resource("50CalAmmo"):
                    cal50 = resources.amount("50CalAmmo")
                ammo = mm20+mm30+cal50
                print("HP:",hp,"Fuel:",fuel,"Ammo:",ammo)
                self.planes.append(Plane(hp,fuel,ammo,hp,fuel,ammo,vessel.name,i,team))
                self.InitialPlanes.append(Plane(hp,fuel,ammo,hp,fuel,ammo,vessel.name,i,team))
                for part in vessel.parts.all:
                    part.tag = str(i)
                i+=1
    def getOld(self,name,i):
        for plane in self.InitialPlanes:
            if plane.id== str(i):
                return plane
        return Plane(0,0,0,0,0,0,name)
    def updatePlanes(self):
        newPlanes = []
        for vessel in self.conn.space_center.vessels:
            try:
                if vessel.parts.with_module("ModuleCommand") and vessel.parts.with_module("MissileFire"):
                    #print(vessel.name)
                    hp = self.getHp(vessel)
                    resources = vessel.resources
                    #print(resources.names)
                    fuel = 0
                    mm20 =0
                    mm30 =0
                    cal50=0
                    if resources.has_resource("LiquidFuel"):
                        fuel = resources.amount("LiquidFuel")
                    if resources.has_resource("20x102Ammo"):
                        mm20 = resources.amount("20x102Ammo")
                    if resources.has_resource("30x173Ammo"):
                        mm30 = resources.amount("30x173Ammo")
                    if resources.has_resource("50CalAmmo"):
                        cal50 = resources.amount("50CalAmmo")
                    ammo = mm20+mm30+cal50
                    #print("HP:",hp,"Fuel:",fuel,"Ammo:",ammo)
                    team = vessel.parts.modules_with_name("MissileFire")
                    team = team[0].get_field('Team')
                    oldPlane = self.getOld(vessel.name,vessel.parts.root.tag)
                    #print((oldPlane.StartHp,oldPlane.StartFuel,oldPlane.StartAmmo,hp,fuel,ammo,vessel.name))
                    newPlanes.append(Plane(oldPlane.StartHp,oldPlane.StartFuel,oldPlane.StartAmmo,hp,fuel,ammo,oldPlane.name,oldPlane.id,team))
            except Exception as e:
                print("Something Destroyed")
        self.planes = newPlanes
    def update(self):
        ret = []
        if self.commandQueue.pop == 'close':
            quit()
        self.updatePlanes()
        for plane in self.planes:
            print(plane.name,"team =",plane.team,"HP:",round(plane.Hp/plane.StartHp*100),"Ammo:",round(plane.Ammo/plane.StartAmmo*100),"Fuel:",round(plane.Fuel/plane.StartFuel*100))
            if plane.Hp/plane.StartHp*100 > 100:
                print (plane.Hp,plane.StartHp)
            ret.append(plane)
        return ret
if __name__ == "__main__":
    main()
