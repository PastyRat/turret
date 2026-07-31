import gui
import logic
import querygui

# Run GUI and get values
chosenvals = gui.main()

# Turn the list back into different variables
coordx = chosenvals[0]
coordy = chosenvals[1]
strength = chosenvals[2]
angle = chosenvals[3]
displacement = chosenvals[4]

print(coordx)
print(coordy)
print(strength)
print(angle)
print(displacement)

# Logic
calculatedvals = logic.solve(coordx, coordy, strength, angle, displacement)
if strength == True: #Check if the user wanted to find the extension or angle and output accordingly
    print("The extension required is", calculatedvals)
else:
    if calculatedvals[0] == 0:
        print("An error occured - invalid values") #add gui when finished
    else:
        print("Angle 1 is", calculatedvals[0])
    if calculatedvals[1] != 0:
        print("Angle 2 is", calculatedvals[1])
    # Create gui to ask the user which angle they want to use if there are multiple angles
    if calculatedvals[1] != 0:
        finalangle = querygui.choicebetweenangles(calculatedvals[0], calculatedvals[1])
    else:
        finalangle = calculatedvals[0]
    print("Angle to be fired at is", finalangle)