#!/usr/bin/python
# -*- coding: UTF-8 -*-
# AUD Übung 8
# Implementieren Sie den Golden-Section-Search-Algorithmus.
# •Schreiben Sie sich zunächst eine Python-Funktion, die die mathematische Funktion enthält,
#  deren Minimum Sie finden wollen. Nehmen Sie als mathematische Funktion (x+1/3)^2
# •Implementieren Sie dann den eigentlichen Suchalgorithmus
# •Überlegen Sie sich ein sinnvolles Abbruchkriterium für die Suche.

import random
import time
from math import sqrt,pow,fabs
import matplotlib.pyplot    
import numpy as np
import pickle
#import audsort
from audsort import BubbleSort, InsertionSort, SelectionSort, mergeSort, quickSort, testListsGenerator
import copy

if __name__ == "__main__":
	max = 200
	randList = []
	#randList.append( testListsGenerator( 1 ) )
	for i in range( 1, max+1 ):
		randList.append( testListsGenerator( i ) )

	# make empty List for results
	Res = []
	sortedLists = []
	SortAlgo = [ BubbleSort, InsertionSort, SelectionSort, mergeSort, quickSort ]
	SortName = [ "BubbleSort", "InsertionSort", "SelectionSort", "mergeSort", "quickSort" ]

	for SortNum in range( len(SortAlgo) ):
		sort = SortAlgo[SortNum]
		print( "Testing %s" % SortAlgo[SortNum].__name__ )
		# make copy of randomList
		workList = []
		workList = copy.deepcopy( randList )
		runTimes = []
		for i in range( len( workList ) ):
			# test runTime of Bubblesort
			StartTime = time.clock()
			sort( workList[i] )
			StopTime = time.clock()
			#print( workList[i] )

			runTime = StopTime - StartTime
			runTimes.append( [i, runTime] )
			#print( "%s %d %f" % ( SortName[SortNum], i, runTime*1000) )
			#runTimes.append( [i, StartTime, StopTime, runTime*1000] )
		Res.append( runTimes )
		sortedLists.append( workList )

	# hier Beweis, dass InsertionSort funktioniert#PrintRes( Res, SortAlgo, SortName )
	'''
	if sortedLists[0] == sortedLists[1]:
		print( "sortedLists[0]==sortedLists[1]" )
	if sortedLists[1] == sortedLists[2]:
		print( "sortedLists[1]==sortedLists[2]" )
	if sortedLists[0] == sortedLists[2]:
		print( "sortedLists[0]==sortedLists[2]" )
	'''
	#SavesortedLists( sortedLists )
	
	
	fig = matplotlib.pyplot.figure()
	# Erzeugen eines axes-Objekts in figure. Dies entspricht der Funktion subplot in Matlab.
	ax = fig.add_subplot(1,1,1)
	# Plotten der Daten innerhalb des axes Objekts.
	#Hier werden zwei Linien mit den Steigungen 2 und 3 erzeugt.

	for SortNum in range( len(SortAlgo) ):
		xwerte = [ i for i in range( 1, max+1 ) ]
		ywerte = [ Res[SortNum][i][1] for i in range( len(Res[SortNum]) ) ]
	#ax.plot( xwerte, ywerte, [min], [TestFunction(min)] )
		ax.plot( xwerte, ywerte )
	#ax.plot( [min], [TestFunction(min)], 'rD' )
	#ywerte = [TestFunction(i) for i in xwerte]
	# Erzeugen einer Legende mit zwei Einträgen.
	ax.legend( [SortName[0], SortName[1], SortName[2], SortName[3], SortName[4]] )
	# Erzeugen der x-Achsen-Beschriftung. Dies entspricht der Funktion xlabel in Matlab.
	ax.set_xlabel('Listlength')
	# Erzeugen der y-Achsen-Beschriftung. Dies entspricht der Funktion ylabel in Matlab.
	ax.set_ylabel('Runtime')
	# min markieren
	# Anzeigen der Grafik in einem Fenster.
	matplotlib.pyplot.show()
