from collections import defaultdict 
import time


UP = 10
DOWN = 15
LEFT = 20
RIGHT = 25
VERTICAL = 100
HORIZONTAL = 101


#trieda pre auto na krizovatke
class Car:
    def __init__(self, farba, velkost, x, y, smer, unik):
        self.farba = farba
        self.velkost = velkost
        self.y = y
        self.x = x
        self.smer = smer
        self.unik = unik

class Pohyb:
    def __init__(self, car, direction, distance):
        self.farba = car.farba
        self.direction = direction
        self.distance = distance
        self.tx = car.x
        self.ty = car.y
    
    def print_pohyb(self):
        print(self.farba, self.direction, self.distance, self.tx, self.ty)

#trieda pre uzol v grafe
class Graph:
    pohyb = None
    unikoveAuto = None
    parent = None
    # Constructor 
    def __init__(self, size): 
  
        # default dictionary to store graph 
        self.sirka = size
        self.dlzka = size
        self.cars = []
        self.krizovatka = [["." for i in range(size)] for j in range(size)]
        
    
  
    # function to add an edge to graph 

    def rovnasa(self, other):
        for i in range(len(self.cars)):
            if(self.cars[i].farba != other.cars[i].farba or self.cars[i].velkost != other.cars[i].velkost or 
                self.cars[i].x != other.cars[i].x or self.cars[i].y != other.cars[i].y 
                or self.cars[i].smer != other.cars[i].smer):
                print("nerovna sa")
                return False        

        print("rovna sa")
        return True    

    #duplikuje uzol
    def duplicate_graph(self):
        newgraph = Graph(self.sirka)
        for i in self.cars:
            c = Car(1, 2, 3, 4, 5, 6)
            c.farba = i.farba
            c.velkost = i.velkost
            c.x = i.x
            c.y = i.y
            c.smer = i.smer
            c.unik = i.unik
            newgraph.pridaj(c)
        return newgraph


    #kontroluje uzol ci je koncovy
    def finish(self):
        #print(self.unikoveAuto)
        x = self.unikoveAuto.x
        y = self.unikoveAuto.y

        for i in range(y + self.unikoveAuto.velkost, self.sirka):
            if self.krizovatka[x][i] != ".":
                return False
        return True


    #prida auto na krizovatku uzla
    def pridaj(self, car):
        x = car.x
        y = car.y
        velkost = car.velkost

        self.cars.append(car)
        if car.unik:
            self.unikoveAuto = car
        if car.smer == "v":
            for i in range(x, (x + velkost)):
                self.krizovatka[i][y] = car.farba
        if car.smer == "h":
            for i in range(y, y + velkost):
                self.krizovatka[x][i] = car.farba
    
    #kontroluje pohyb po krizovatke vrcia ci sa moye alebo nemoze pohnut
    def can_move(self, car, direction, distance):
            if direction == UP:
                if car.smer == "h" or car.x - distance < 0:
                    return False
                for i in range(car.x - distance, car.x):
                    if self.krizovatka[i][car.y] != ".":
                        return False
                return True,
            if direction == DOWN:
                if car.smer == "h" or car.x + car.velkost - 1 + distance >= self.dlzka:
                    return False
                for i in range(car.x + car.velkost, car.x + car.velkost+distance):
                    if self.krizovatka[i][car.y] != ".":
                        return False
                return True,
            if direction == LEFT:
                if car.smer == "v" or car.y - distance < 0:
                    return False
                for i in range(car.y - distance,  car.y):
                    if self.krizovatka[car.x][i] != ".":
                        return False
                return True,
            if direction == RIGHT:
                if car.smer == "v" or car.y + car.velkost - 1 + distance >= self.sirka:
                    return False
                for i in range(car.y + car.velkost, car.y + distance + car.velkost):
                    if self.krizovatka[car.x][i] != ".":
                        return False
                return True,
    
    #hybe autom po krizovatke
    def move(self, origi_car, direction, distance):
        car = Car(1, 2, 3, 4, 5, 6)
        
        car.farba = origi_car.farba
        car.velkost = origi_car.velkost
        car.x = origi_car.x
        car.y = origi_car.y
        car.smer = origi_car.smer
        car.unik = origi_car.unik


        if direction == UP:
            direction = 'up'
            for i in range(0, car.velkost):
                self.krizovatka[car.x + i][car.y] = "."
            for i in range(0, car.velkost):
                self.krizovatka[car.x + i - distance][car.y] = car.farba
            for c in self.cars:
                if c.farba == car.farba:
                    c.x -= distance
                    break    
            


        if direction == DOWN:
            direction = 'down'
            for i in range(0, car.velkost):
                self.krizovatka[car.x + i][car.y] = "."
            for i in range(0, car.velkost):
                self.krizovatka[car.x + i + distance][car.y] = car.farba
            for c in self.cars:
                if c.farba == car.farba:
                    c.x += distance
                    break
            

        if direction == LEFT:
            direction = 'left'
            for i in range(0, car.velkost):
                self.krizovatka[car.x][car.y + i] = "."
            for i in range(0, car.velkost):
                self.krizovatka[car.x][car.y + i - distance] = car.farba
            for c in self.cars:
                if c.farba == car.farba:
                    c.y -= distance
                    break

        if direction == RIGHT:
            direction = 'right'
            for i in range(0, car.velkost):
                self.krizovatka[car.x][car.y + i] = "."
            for i in range(0, car.velkost):
                self.krizovatka[car.x][car.y + i + distance] = car.farba
            for c in self.cars:
                if c.farba == car.farba:
                    c.y += distance
                    break
            
        self.pohyb = Pohyb(car, direction, distance)
        
        
            
    #generuje vsetky mozne kroky a vytvori pre nich uzly
    def generate_all_moves(self):
        moves = []
        for car in self.cars:
            for distance in range(1, 5):
                if car.smer == "v":
                    if self.can_move(car, UP, distance):
                        x = self.duplicate_graph()
                        x.move(car, UP, distance)
                        x.parent = self
                        moves.append(x)
                    if self.can_move(car, DOWN, distance):
                        x = self.duplicate_graph()
                        x.move(car, DOWN, distance)
                        x.parent = self
                        moves.append(x)
                    if self.can_move(car, UP, distance) == False and self.can_move(car, DOWN, distance) == False:
                        break
                if car.smer == "h":
                    if self.can_move(car, LEFT, distance):
                        x = self.duplicate_graph()
                        x.move(car, LEFT, distance)
                        x.parent = self
                        moves.append(x)
                    if self.can_move(car, RIGHT, distance):
                        x = self.duplicate_graph()
                        x.move(car, RIGHT, distance)
                        x.parent = self
                        moves.append(x)
                    if self.can_move(car, LEFT, distance) == False and self.can_move(car, RIGHT, distance) == False:
                        break
        return moves



def print_unik(uzol):
    for riadok in uzol.krizovatka:
        print(riadok)

#kontroluje ci uzol uz bol navstiveny
def is_visited(visited, uzol):
    for i in visited:
            if i.krizovatka == uzol.krizovatka:
                return True
    return False

#prehladavanie do sirky
def BFS(uzol):
    kroky = 0
    fronta = []
    visited = []
    fronta.append(uzol)
    while fronta:
        x = fronta.pop(0)
        if x.finish():
            print("riesenie")
            for i in x.cars:
                print(i.farba, i.velkost, i.x + 1, i.y + 1, i.smer)
            zaloha = x
            while x.parent != None:
                x.pohyb.print_pohyb()
                x = x.parent
                kroky += 1
            print_unik(zaloha)
            print("++++++++++++")
            print_unik(x)
            print("riesenie BFS v" + str(kroky))
            return
        if  is_visited(visited, x):
            continue
        else:
            visited.append(x)
            uzly = x.generate_all_moves()
            fronta = fronta + uzly
    print_unik(x)
    print("Nema riesienie")

#prehladavanie do hlbky
def DFS(uzol):
    #kroky = 0
    visited = []
    stack = []

    stack.append(uzol)

    while stack:
        kroky = 0
        x = stack.pop(len(stack)-1)
        if x.finish():
            zaloha = x
            while x.parent != None:
                x.pohyb.print_pohyb()
                x = x.parent
                kroky += 1
            print_unik(zaloha)
            print("++++++++++++")
            print_unik(x)
            print("riesenie DFS v " + str(kroky))
            return
        if  is_visited(visited, x):
            continue
        else:
            visited.append(x)
            uzly = x.generate_all_moves()
            for i in uzly:
                stack.append(i)
            #stack = stack + uzly
    print_unik(x)
    print("Nema riesienie")


def nacitaj_uzol():
    uzol = Graph(6)
    cars = []
    f = open(r'D:\skola\3_rocnik20202021\zs20202021\UI\zadanie2_UI_M_Rudolf\subor.txt', "r")
    for i in f:
        smer = i[-2]
        x = int(i[4])-1
        y = int(i[6])-1
        velkost = int(i[2])
        farba = i[0]
        if farba == '!':
            unik = True
        else:
            unik = False
        cars.append(Car(farba, velkost, x, y, smer, unik))
    f.close()
    for car in cars:
        uzol.pridaj(car)
    return uzol    


uzol = nacitaj_uzol()
start = time.time()
#BFS(uzol)
BFS(uzol)
end = time.time()
print("%.5gs" % (end-start))