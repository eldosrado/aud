#!/usr/bin/python
# -*- coding: UTF-8 -*-

from FloodFill import StripLineEnd, ReadField, PrintField
from FloodFill import emptyMarker, filledMarker, specialMarker, EscapeMarker
import numpy as np
import os
import copy

NumTrys = 0
InstanceCount = 0
#Debug = False

def inField( Field, rowNumber, columnNumber ):
	LeftBorder = 0
	RightBorder = len(Field[0])-1
	TopBorder = 0
	BottomBorder = len( Field )-1
	if columnNumber < LeftBorder or columnNumber > RightBorder or \
			rowNumber < TopBorder or rowNumber > BottomBorder:
		return False
	return True

def isFree( Field, rowNumber, columnNumber ):
	if not inField( Field, rowNumber, columnNumber ):
		return False
#-	if Field[rowNumber][columnNumber] != emptyMarker:
#-		return False
#-	return True
	if Field[rowNumber][columnNumber] == filledMarker:
		return False
	return True

def isEscape( Field, rowNumber, columnNumber ):
	if not inField( Field, rowNumber, columnNumber ):
		return False
	if Field[rowNumber][columnNumber] != EscapeMarker:
		return False
	return True

def printRoute( Field, route ):
	Field = copy.deepcopy( Field )
	for pos in route:
		Field[ pos[0] ][ pos[1] ] = '#'
	if os.name == "nt":
		os.system( "cls" )
	else:
		os.system( "clear" )
	PrintField( Field )

def findEscape( Field, rowNumber, columnNumber, route=() ):
	global NumTrys
	'''
	NumTrys = NumTrys + 1
	if NumTrys > 500:
		print( "max NumTrys erreicht" )
		return list()
		raise Exception( "max NumTrys erreicht" )
	'''
	
	# format (y,x).    >,      <,      ^,     v
	richtung = ( (0,1), (0,-1), (-1,0), (1,0) )
	pos = ( rowNumber, columnNumber )
	
	
	listroute = list( route )
	listroute.append( pos )
	route = tuple( listroute )
	printRoute( Field, route )
	
	if isEscape( Field, rowNumber, columnNumber ):
		#print( "gefunden", route )
		return list(route)
	else:
		#for k' in nachbarn:
		Nachbarn = []
		for n in richtung:
			temp = tuple( np.add( (rowNumber, columnNumber), n ) )
			if isFree( Field, temp[0], temp[1] ):
				Nachbarn.append( temp )
		
		# nicht zurück gehen
		nichtBesucht = []
		for FreierNachbar in Nachbarn:
			if not FreierNachbar in route:
				nichtBesucht.append( FreierNachbar )
		
		result = []
		for k in nichtBesucht:
			temp = findEscape( Field, k[0], k[1], route )
			if temp != []:
				if len(temp) > 0 and isinstance( temp[0], list ):
					for row in temp:
						result.append( row )
				else:
					result.append( temp )
		
		if len( result ) > 0:
			return result
		else:
			return list()

if __name__ == "__main__":
	#fileName = "TestField1.txt"		#spirale
	#fileName = "TestField2.txt"		#klein
	#fileName = "TestField3.txt"		#groß
	fileName = "TestField4.txt"		#mittel
	
	TestField = ReadField( fileName )
	PrintField( TestField )
	
	#global InstanceCount
	InstanceCount = 0
	result = findEscape( TestField, 1, 1 )

	best = result[0]
	for row in result:
		if len(row) < len(best):
			best = row
	
	printRoute( TestField, best )
	print("Beste Route mit %d Schritten" % len(best) )
	print(best)

	print( "%d Routen gefunden" % len(result) )
	for row in result:
		print( ">", row )
		print("")
