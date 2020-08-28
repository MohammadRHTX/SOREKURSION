import matplotlib.pyplot as plt
import numpy as np
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from matplotlib.widgets import Button

def findDerivative(mathFunction):
    try:
        prime_function = diff(mathFunction)
        return prime_function, true
    except:
        prime_function = "ERROR"
        return prime_function, false

def funcCheck(function):
    acceptedSymbols = "0123456789*+-/.xy costansin()log"

    for index, n in enumerate(function):
        if(n in acceptedSymbols):
            if (index == function.index(function[-1])):
                return True

        else:
            return False

def newtonsMethod(start_value, mathFunction , derivative):
    list_of_x_values = []

    before_x = start_value

    for _ in range(1000):
        exprs = eval((mathFunction.replace("x", str(before_x)))) / eval((str(derivative).replace("x", str(before_x))))
        x = before_x - (exprs)
        before_x = x
        list_of_x_values.append(x)

    return list_of_x_values

functionMath = "2*x**3 + (x-100) + 1"

SymbolConvertDict = {"x": Symbol("x", real=True)}

funcDiff, booleanDiff = findDerivative(parse_expr(functionMath, SymbolConvertDict))
authorized = funcCheck(functionMath)

if(authorized):
    print("Indtast startbetingelse: ")

    while 1:
        startValue = input("Enter: ")
        if(startValue.isdigit()):
            startValue = float(startValue)
            break
        else:
            print(" ** Startbetingelsen skal være et tal! \b Prøv igen \b ** ")

    newTonsX = newtonsMethod(startValue, functionMath, funcDiff)

    y_values_function = []
    slope_y_values_diff = []
    x_values = np.linspace(-100, 100, 1000)

 #   print(list(x_values))

    for n in x_values:
        # DETERMINE Y VALUES FOR THE MATH FUNCTION
        y_raw = functionMath.replace("x", f"({str(n)})")
        y = eval(y_raw)
        y_values_function.append(y)

        # DETERMINE THE SLOPE OF PRIME FUNCTION
        slope_raw_diff = str(funcDiff).replace("x", f"({str(n)})")
        slope_diff = eval(slope_raw_diff)
        slope_y_values_diff.append(slope_diff)

    plt.figure(figsize=(8, 5))

    p, = plt.plot(x_values, slope_y_values_diff, label="Differentialkvotient", linewidth=2)
    b, = plt.plot(x_values, y_values_function, label="Funktion", linewidth=2)

    # GRAPH SETTINGS
    ax = plt.gca()

    plt.subplots_adjust(bottom=0.3)

    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')

    plt.legend([p,b], ("Differentialkvotient", "Funktion"))

    tan_y = []
    tan_b = []
    tan_a = []

    # FIND TAN LINE AND PLOTTING
    for xv in newTonsX:

        y_raw = functionMath.replace("x", f"({str(xv)})")
        y = eval(y_raw)
        tan_y.append(y)

        slope_raw_diff = str(funcDiff).replace("x", f"({str(xv)})")
        slopes = eval(slope_raw_diff)
        tan_a.append(slopes)

    # FIND THE B VALUE
    for x,y, a in zip(newTonsX, tan_y, tan_a):
        b = y - a * x
        tan_b.append(b)

    tanLinearY = []
    num = 0
    lines = []
    attempts = 0

    def nextStepfunc(event):
        global attempts
        global num
        global x_values
        if(attempts <= 0):
            ax.lines.pop(0)

        attempts += 1

        for _ in range(1):
            tanLinearY = []

            if(len(lines) >= 1):
                ax.lines.pop()
                ax.lines.pop()

            for x in x_values:
                y = tan_a[0] * x + tan_b[0]
                tanLinearY.append(y)

            t = ax.plot(x_values, tanLinearY, linestyle="--")
            t[0].set_label("Tangent")
            lines.append(t)

            rightAngelX = [newTonsX[num], newTonsX[num]]
            rightAngelY = [tan_y[num], 0]

            a = ax.plot(rightAngelX, rightAngelY)
            lines.append(a)

            print("Information om tangenten")
            print(f"Hældning: {tan_a[0]}")
            print(f"Skærings med y-aksen: {tan_b[0]}")
            print(f"X: {newTonsX[num]}")
            print(f"Y: {tan_y[0]}")
            print("--------------------------")
            print("Newtons metode")
            print(f"x værdi: {newTonsX[num]}")
            print(f"Antal forsøg: {attempts}")
            print("--------------------------")

            del tan_b[0]
            del tan_a[0]
            del tanLinearY[0]

        num += 1

     #   ax.xaxis.zoom(-7 + num)
     #   ax.yaxis.zoom(-7 + num)

    ax_img = plt.axes([0.45, 0.1, 0.1, 0.1]) # left, bottom, width, height

    btn = Button(ax=ax_img,
                 label="NEXT STEP",
                 color="teal",
                 hovercolor="tomato")

    btn.on_clicked(nextStepfunc)
    plt.show()

else:
    print("NOT AUTHORIZED")