#!/usr/bin/python
# -*- coding: UTF-8 -*-
# AUD Übung 8
# Implementieren Sie den Golden-Section-Search-Algorithmus.
# •Schreiben Sie sich zunächst eine Python-Funktion, die die mathematische Funktion enthält,
#  deren Minimum Sie finden wollen. Nehmen Sie als mathematische Funktion (x+1/3)^2
# •Implementieren Sie dann den eigentlichen Suchalgorithmus
# •Überlegen Sie sich ein sinnvolles Abbruchkriterium für die Suche.

#import math

import random
from math import sqrt,pow,fabs

def BubbleSort( workList ):
	for k in range( len(workList)-1, 0, -1 ):
		sorted = True
		for i in range( 0, k ):
			if workList[i] > workList[i+1]:
				workList[i], workList[i+1] = workList[i+1], workList[i]
				sorted = False
		# stop if allElements are sorted
		if sorted:
			break
	# allElements are sorted
	return workList

def InsertionSort( workList ):
	for k in range( 1, len(workList) ):
		# store current element
		key = workList[k]
		i = k-1
		while i >= 0 and workList[i] > key:
			workList[i+1] = workList[i]
			i = i-1
		# insert sored element
		workList[i+1] = key
	
	return workList

def SelectionSort( workList ):
	for j in range( 0, len(workList) ):
		minIndex = j
		for i in range( j+1, len(workList) ):
			if workList[i] < workList[minIndex]:
				minIndex = i
		workList[j], workList[minIndex] = workList[minIndex], workList[j]
	
	return workList

def testListsGenerator( Length ):
	# Numbers from 0 to NumberRange
	NumberRange = 1000
	workList = []

	for i in range( Length ):
		randomNumber = int( random.random() * NumberRange )
		workList.append( randomNumber )

	return workList

def TestSort( SortAlgorithm, randomList, sortedList ):
	sortedListbySort = SortAlgorithm( randomList )
	if sortedListbySort == sortedList:
		print( "%s Test Passed" % SortAlgorithm.__name__ )
	else:
		print( "%s Test Failed" % SortAlgorithm.__name__ )
	print( "randomList      " , randomList )
	print( "sortedListbySort" , sortedListbySort )
	return sortedListbySort

def Test():
	randomList = [ 9, 1, 6, 7, 3, 0, 10, 2, 4, 8, 5, 11, 12, 13, 42, 17, 4, 7, 101, 3 ]
	sortedList = [ 0, 1, 2, 3, 3, 4, 4, 5, 6, 7, 7, 8, 9, 10, 11, 12, 13, 17, 42, 101 ]
	TestSort( BubbleSort, randomList[:], sortedList )
	TestSort( InsertionSort, randomList[:], sortedList )
	TestSort( SelectionSort, randomList[:], sortedList )

if __name__ == "__main__":
	randomList = [ 9, 1, 6, 7, 3, 0, 10, 2, 4, 8, 5, 11, 12, 13, 42, 17, 4, 7, 101, 3 ]
	Test()
	print("")
	testList = randomList[:]
	randomList[0] = 200
	print( InsertionSort( testList ) )
	print( randomList )
	print( InsertionSort( randomList ) )
	print( randomList )
	#testList = testListsGenerator( 12 )
	#print( "testList     =", randomList )
	#print( "BubbleSort   =", BubbleSort( randomList[:] ) )
	#print( "testList     =", testList )
	#print( "InsertionSort=", InsertionSort( randomList[:] ) )
	#print( "testList     =", testList )
	#print( "SelectionSort=", SelectionSort( randomList[:] ) )
	#print( "testList     =", testList )
