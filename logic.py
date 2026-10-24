import math
interval = 0.001
p = 1.225
C = 0.4
A = 0.0025
m = 0.4
k = 12000
u = 0.3
g= 9.80665
tolerance=0.001
global Angle1
global Angle2
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
    solution = aproximate(p,C,A,m,k,u,h,g,Decision,coordinateX,coordinateZ, strength)
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
def model(p,C,A,a,m,k,x,u,h,g):
    SpringInterval = 0.0001#smaller time step for spring to improve accuracy
    s = 0
    V0 = 0
    y = h
    t= 0
    while x>=0:
        def acceleration(extension,velocity):
            return (
                k*extension
                - m*u*g*math.cos(a)
                - 0.5*p*C*A*velocity**2
                - m*g*math.sin(a)
            ) / m
        a1 = acceleration(x, V0)
        x_mid = x - 0.5*V0*SpringInterval
        v_mid = V0 + 0.5*a1*SpringInterval
        a_mid = acceleration(x_mid, v_mid)
        x_new = x - v_mid*SpringInterval
        v_new = V0 + a_mid*SpringInterval
        if x_new <= 0:
            fraction = x / (x - x_new)
            V0 += fraction*(v_new - V0)
            x = 0
            break
        x = x_new
        V0 = v_new
    Vx = V0*math.cos(a)
    Vy = V0*math.sin(a)
    run = 1
    if h > 0:
        run = 0
    l=y
    while y>=0 or run != 0:
        if y >=0 and h <=0 and run == 1:
            run = 0
        if y<l and y<0 and run==1:
            return -1
            break
        B = Vy
        D = Vx
        Vy = (-g-((p*C*A)/(2*m))*((Vx**2+Vy**2)**(1/2))*Vy)*interval+Vy
        Vx = (-((p*C*A)/(2*m))*((Vx**2+B**2)**(1/2))*Vx)*interval+Vx
        l=y
        y=B*interval+y
        s = D*interval +s
    return s

def aproximate(p,C,A,m,k,u,h,g,Decision,coordinateX,coordinateZ, strength):
    global x
    global a
    if Decision == 1:
        List=[]
        #x = float(input("enter band distance: "))
        x = strength
        Displacement = (coordinateX**2+coordinateZ**2)**(1/2)
        print("distance needed",Displacement)
        for i in range(0,45001):
            Values2=[]
            angle=i/500
            value = model(p,C,A,math.radians(angle),m,k,x,u,h,g)
            if abs(value - Displacement)<=tolerance:
                Values2.append(value)
                Values2.append(angle)
                List.append(Values2)
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
        value = model(p,C,A,a,m,k,x,u,h,g)
        print("distance needed",Displacement)
        while round(value,2) != round(Displacement,2) and i <=4000:

            i = i +1
            if value < Displacement:
                x1 = x
            if value> Displacement:
                x2 = x
            x = (x1+x2)/2
            value = model(p,C,A,a,m,k,x,u,h,g)
           
       
        if i >=4000:
            print("Unable to aproximate. Value for extension may work and be used but distance may not round to the same 1cm")
        return x
if __name__ == "__main__":
    print(solve(20,20,0.1,0))