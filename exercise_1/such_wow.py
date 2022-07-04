import sys


if (len(sys.argv) != 3):
    print("Error input args")
    exit()
elif (sys.argv[1].isnumeric()==False or sys.argv[2].isnumeric()==False):
    print("Error input is not a number")
    exit()
elif (int(sys.argv[1]) >= int(sys.argv[2])):
    print("First number must be minor than second number")
    exit()

output = []

for i in range (int(sys.argv[1]), (int(sys.argv[2]) + 1) ):
    i = int(i) 
    if (i%3 == 0 and i%5 != 0):
        output.append("Such")
    elif (i%3 != 0 and i%5 == 0):
        output.append("Wow")
    elif (i%3 == 0 and i%5 == 0):
        output.append("SuchWow")
    else:
        output.append(i)

print(output)