#!/usr/bin/python
# -*- coding: UTF-8 -*-
# AUD Übung 8
# Implementieren Sie den Golden-Section-Search-Algorithmus.
# •Schreiben Sie sich zunächst eine Python-Funktion, die die mathematische Funktion enthält,
#  deren Minimum Sie finden wollen. Nehmen Sie als mathematische Funktion (x+1/3)^2
# •Implementieren Sie dann den eigentlichen Suchalgorithmus
# •Überlegen Sie sich ein sinnvolles Abbruchkriterium für die Suche.

#import math

from math import sqrt,pow,fabs
import matplotlib.pyplot    
import numpy as np

# return y = f(x)
def TestFunction(x):
    x = float(x)
    y = pow( x+1.0/3, 2.0)
    return y
    
def GetDeltaX( Left, Right ):
    Temp = 2 / (3+sqrt(5))
    DeltaX = Temp * (Right-Left)
    return DeltaX
    
    
# search min in @function in Intervall Left < Right
# stops at function(min)+delta
# returns min +-delta
def GoldenSectionSearch( function, Left, Right, delta):
    #phi = ( 1 + sqrt(5)) / 2
    print( "Start with Left=%f Right=%f delta=%f" %(Left,Right,delta) )
    #mL = Left
    #mR = Right
    #print("1.")
    YfromLeft     = TestFunction( Left )
    YfromRight    = TestFunction( Right )
      
    #DeltaX = GetDeltaX( Left, Right )
    mL = Left  + GetDeltaX( Left, Right )
    mR = Right - GetDeltaX( Left, Right )
    
    YfromNewLeft  = function( mL )
    YfromNewRight = function( mR )
    print( "Left=%f mL=%f mR=%f Right=%f" %( Left,mL,mR,Right) )
    print( "f(mL)=%f f(mR)=%f" % (YfromNewLeft,YfromNewRight) )
    print( "")
      
    while( fabs(YfromNewLeft-YfromNewRight) > delta ):
        if YfromNewLeft < YfromNewRight:
            # Minimum in Intervall Left,newRight
            # x werte übenehmen
            Left = Left
            Right = mR
            mR = mL
            # y werte übernehmen
            YfromLeft     = YfromLeft
            YfromRight    = YfromNewRight
            YfromNewRight =YfromNewLeft
                
            #mL = neu berechnen
            mL = Left  + GetDeltaX( Left, Right )
            YfromNewLeft = function( mL )
        else:
            # Minimum in Intervall mL,Right
            # x werte übenehmen
            Right = Right
            Left = mL
            mL = mR
            # y werte übernehmen
            YfromRight   = YfromRight
            YfromLeft    = YfromNewLeft
            YfromNewLeft = YfromNewRight
            #mR = neu berechnen
            mR = Right - GetDeltaX( Left, Right )
            YfromNewRight = function( mR )
          
        print( "Left=%f mL=%f mR=%f Right=%f" %( Left,mL,mR,Right) )
        print( "f(mL)=%f f(mR)=%f" % (YfromNewLeft,YfromNewRight) )
        print("")
    min = (mR-mL) / 2.0 + mR
    return min
    
## just print some values from TestFunction
#for i in range(-3,4,1):
#    y = TestFunction( i )
#    print( "y = f(%f) = %f" % (i,y) )
    
if __name__ == "__main__":
    min = GoldenSectionSearch( TestFunction, -3, 3, 0.00000000001 )
    print( "min=%f" % min )
    
    fig = matplotlib.pyplot.figure()
    # Erzeugen eines axes-Objekts in figure. Dies entspricht der Funktion subplot in Matlab.
    ax = fig.add_subplot(1,1,1)
    # Plotten der Daten innerhalb des axes Objekts.
    #Hier werden zwei Linien mit den Steigungen 2 und 3 erzeugt.
    
    #numbers=list(range(0,10))
    #ax.plot(numbers, [i*2 for i in numbers], numbers, [i*3 for i in numbers])

    #xwerte = list( xrange(-3,3,0.1) )
    xwerte = np.arange( -3.0, 3, 0.1)
    ywerte = [ TestFunction(x) for x in xwerte ]
    #ax.plot( xwerte, ywerte, [min], [TestFunction(min)] )
    ax.plot( xwerte, ywerte )
    ax.plot( [min], [TestFunction(min)], 'rD' )
    #ywerte = [TestFunction(i) for i in xwerte]
    # Erzeugen einer Legende mit zwei Einträgen.
    ax.legend(["(x+1/3)^2"])
    # Erzeugen der x-Achsen-Beschriftung. Dies entspricht der Funktion xlabel in Matlab.
    ax.set_xlabel('x')
    # Erzeugen der y-Achsen-Beschriftung. Dies entspricht der Funktion ylabel in Matlab.
    ax.set_ylabel('y')
    # min markieren
    # Anzeigen der Grafik in einem Fenster.
    matplotlib.pyplot.show()
    
