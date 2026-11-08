import gui
import logicrs as logic
import querygui
import send

# Connect to the arduino
if send.startconnection() == 0:
    print("Stopping program")
    exit()

# Run GUI and get values
chosenvals = gui.main()

# Turn the list back into different variables
coordx = chosenvals[0]
coordy = chosenvals[1]
displacement = chosenvals[2]

# Spring strength
strength = 0.1

print(coordx)
print(coordy)
print(strength)
print(displacement)

xzangle = logic.find_xzangle(coordx, coordy)
print("The angle in the 2d plane is", xzangle)

# Logic
calculatedvals = logic.solve(coordx, coordy, strength, displacement)
if calculatedvals[0] == 0:
    print("An error occured - invalid values") #add gui when finished
else:
    print("Angle 1 is", calculatedvals[0])
if calculatedvals[1] != 0:
    print("Angle 2 is", calculatedvals[1])
    # Create gui to ask the user which angle they want to use if there are multiple angles
    finalangle = querygui.choicebetweenangles(calculatedvals[0], calculatedvals[1])
else:
    finalangle = calculatedvals[0]
finalangle = -finalangle
print("Angle to be fired at is", finalangle)
print("Sending values to Arduino...")
send.send(xzangle, finalangle, strength)