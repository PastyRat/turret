import math
#Constants
p = 1.225
A = 0.0025
m = 0.2
k = 12000
u = 0.3
g= 9.80665
tolerance=0.01
r=((A)/(2*math.pi))**(1/2)
angleaccuracy = 0.005 #make sure this gives an int if / by 90 for best search
interval = 0.0005
springint = 0.000003
mnest = 0.01
mspring = 0.1
mgrav = mnest+(mspring/2)+m # mass of spring accounter for in launch. (1) is its mass the other value is the nest's mass
meff = mnest+(mspring/3)+m #mass of spring for acceleration
def find_xzangle(coordinateX, coordinateZ):
    angle = math.degrees(math.atan2(coordinateZ, coordinateX))
    if angle < 0:
        angle += 360
    return angle

def solve(coordinateX, coordinateZ, strength, displacement):
    #coordinateX = float(input("enter x: "))
    #coordinateZ = float(input("enter z: "))
    #h = float(input("enter displacement: "))
    h = displacement
    #Decision = int(input("input band distance and find angle or input angle and find band distance? 1 or 2: "))
    # Hardcode decision
    Decision = 1
    angle = 0
    solution = aproximate(p,A,m,k,u,h,g,r,Decision,coordinateX,coordinateZ, strength)
    if Decision == 1:
        T1 =0
        N1=0
        T2=0
        N2=0
        for i in range(0,len(solution)):
            if abs(solution[0][1]-solution[i][1]) <=1:
                T1 = T1 + solution[i][1]
                N1=N1+1
            else:
                T2 = T2 + solution[i][1]
                N2=N2+1
        if N1!=0:
            Angle1=T1/N1
            #print("one angle is ",Angle1)
        if N2!=0:
            Angle2=T2/N2
            #print("one angle is",Angle2)
        else:
            Angle2 = 0
        if N2 == 0 and N1 ==0:
            print("no solution")
        return [Angle1, Angle2]
    if Decision ==2:
        x = solution
        if x <=0.5:
            #print("band extension needed is",x)
            return x
        else:
            print("no solution within range")
def model(p,A,a,m,k,x,u,h,g,r):
    err = 0
    Vy=0
    Vx=0
    s=0
    y=h
    V0=0
    B=0
    while x>=0:
        Re = (p*V0*2*r)/(1.81*10**-5) #viscosity
        
        if V0<=10:
            c=0.47
        else:
            c = (24.0 / Re) + (2.6 * (Re / 5.0)) / (1.0 + (Re / 5.0)**1.52) + (0.411 * (Re / 2.63e5)**-7.94) / (1.0 + (Re / 2.63e5)**-8.00) + (0.25 * (Re / 1e6)) / (1.0 + (Re / 1e6))
        V0 = (((k * x) - (mgrav * g * math.sin(a)) - (m * g * math.cos(a) * u) - (0.5 * p * (V0**2) * c * A)) / meff) * springint + V0
        x=x-((V0+B)/2)*springint
        B=V0
    Vx=V0*math.cos(a)
    Vy=V0*math.sin(a)
    B=Vy
    D=Vx
    fix = 0
    if y <0:
        fix = 1
    while y>= 0 or fix == 1:
        Re = (p*((Vx**2+Vy**2)**(1/2))*2*r)/(1.81*10**-5)
        if (Vx**2+Vy**2)**(1/2)<=10:
            c=0.47
        else:
            c = (24.0 / Re) + (2.6 * (Re / 5.0)) / (1.0 + (Re / 5.0)**1.52) + (0.411 * (Re / 2.63e5)**-7.94) / (1.0 + (Re / 2.63e5)**-8.00) + (0.25 * (Re / 1e6)) / (1.0 + (Re / 1e6))
        Vy = (-g-((p*c*A)/(2*m))*((Vx**2+Vy**2)**(1/2))*Vy)*interval+Vy
        Vx = (-((p*c*A)/(2*m))*((Vx**2+Vy**2)**(1/2))*Vx)*interval+Vx
        s = s + ((Vx+D)/2)*0.0005
        h=y
        y=y+interval*((Vy+B)/2)
        B=Vy
        D=Vx
        if y<h and fix == 1:
            err = 1
            break
        if y>=0 and fix ==1:
            fix = 0
    if err != 1:
        return s
    else:
        return 0

def aproximate(p,A,m,k,u,h,g,r,Decision,coordinateX,coordinateZ, strength):
    global x
    global maxs
    maxs =0 #max distance
    if Decision == 1:
        List=[]
        #x = float(input("enter band distance: "))
        x = strength
        Displacement = (coordinateX**2+coordinateZ**2)**(1/2)
        print("distance needed",Displacement)
        for i in range(0,int(90/angleaccuracy+1)):
            Values2=[]
            angle=i*angleaccuracy
            value = model(p,A,math.radians(angle),m,k,x,u,h,g,r)
            if abs(value - Displacement)<=tolerance:
                Values2.append(value)
                Values2.append(angle)
                List.append(Values2)
            if maxs < value:
                maxs=value
        return List
       
    else:
        selectedangle = 0
        print("this shouldn't ever be ran")
        a = math.radians(float(selectedangle))
        Displacement = (coordinateX**2+coordinateZ**2)**(1/2)
        x1 = 0
        x2 = 0.5
        i=0
        x = (x1+x2)/2
        value = model(p,C,A,a,m,k,x,u,h,g,r)
        print("distance needed",Displacement)
        while round(value,2) != round(Displacement,2) and i <=4000:

            i = i +1
            if value < Displacement:
                x1 = x
            if value> Displacement:
                x2 = x
            x = (x1+x2)/2
            value = model(p,A,a,m,k,x,u,h,g,r)
           
       
        if i >=4000:
            print("Unable to aproximate. Value for extension may work and be used but distance may not round to the same 1cm")
        return x
if __name__ == "__main__":
    print(solve(15,20,0.1,0))    
