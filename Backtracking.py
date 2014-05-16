#!/usr/bin/python
# -*- coding: UTF-8 -*-

from FloodFill import StripLineEnd, ReadField, PrintField
from FloodFill import emptyMarker, filledMarker, specialMarker, EscapeMarker
import numpy as np

# row Zeile, rowNumber = y
# coumn Spalte, columnNumber = x
#                 , y        , x
def inField( Field, rowNumber, columnNumber ):
	LeftBorder = 0
	RightBorder = len(Field[0])-1
	TopBorder = 0
	BottomBorder = len( Field )-1
	#print( "isFree %d %d LR %d-%d TD %d-%d " % (columnNumber, rowNumber, LeftBorder, RightBorder, TopBorder, BottomBorder) , end='')
	if columnNumber < LeftBorder or columnNumber > RightBorder or rowNumber < TopBorder or rowNumber > BottomBorder:
		return False
	return True

#                , y        , x
def isFree( Field, rowNumber, columnNumber ):
#	print( "isFree %d %d " % (rowNumber, columnNumber) , end='')
	if not inField( Field, rowNumber, columnNumber ):
#		print( "false" )
		return False
	if Field[rowNumber][columnNumber] != emptyMarker:
#		print( "false" )
		return False
	
#	print( "true" )
	return True

#                  , y        , x
def isEscape( Field, rowNumber, columnNumber ):
#	print( "isEscape %d %d " % (rowNumber, columnNumber) , end='')
	if not inField( Field, rowNumber, columnNumber ):
#		print( "false" )
		return False
	if Field[rowNumber][columnNumber] != EscapeMarker:
#		print( "false" )
		return False
#	print( "true" )
	return True

def visited( route, pos ):
	for row in route:
		#if pos in row[0]:#geht nicht
		if pos == row[0]:
			return True
	return False

def isDeadEnd( pos ):
	return False

def isKnownRoute( pos ):
	return False

def printRoute( route ):
	for row in route:
		print( row )

def goBack( route ):
	Removed = []
	currentPos = route[-1][0]
	while currentPos == []:
		# route kürzen
		route = route[:-1]
		# zu entfernendes element in seperate Liste eintragen
		currentPos = route[-1][0]
		Removed.append( currentPos )
		if currentPos == []:
			break
		# element entfernen
		route[:-1] = route[-1][1:]

def findEscape( Field, rowNumber, columnNumber, route=[] ):
	# format (y,x).    >,      <,      ^,     v
	neighbours = ( (0,1), (0,-1), (-1,0), (1,0) )
	Steps = 0
#	print( "--------------------" )
#	print( route )
	#print( "z=%d s=%d %s" % (rowNumber, columnNumber, "suche") )

	if len(route) == 0 :
		route.append( [(rowNumber,columnNumber)] )
	currentPos = route[-1]
	print( "%s %s" % (currentPos, "Hallo ich bin Lara und ich muss jetzt durch dieses Labyrinth") )
	PrintField( Field )
	
	while len(route) > 0 :
		# TODO: remove Steps. Only needed for debugging
		Steps = Steps + 1
		if Steps > 50:
			return

		currentPos = route[-1][0]
		# teste, ob wir in einer Sackgasse stecken
		if currentPos == []:
			goBack( route )
		
		# teste alle Nachbarn
		newWays = []
		for n in neighbours:
			Pos = tuple( np.add( currentPos, n ) )
			# sind wir schon da?
			if isEscape( Field, rowNumber=Pos[0], columnNumber=Pos[1] ):
				# Ausgang gefunden route ausgeben, bzw merken
				#print( "z=%d s=%d %s" % (Row, Column, "Ausgang gefunden") )
				#newRoute = route[:]
				#newRoute.append( (Row,Column) )
				#print( "**********************************" )
				#print( len(newRoute) )
				#print( newRoute )
				#print( "**********************************" )
				#gefundeneRouten.append( [len(newRoute), newRoute] )
				#return True
				pass

			# ist nachbar frei
			if isFree( Field, rowNumber=Pos[0], columnNumber=Pos[1] ):
				if visited( route, Pos ):
					print( "%s %s" % (Pos, "hier war ich schon") )
					#try next neighbour
					continue
				if isDeadEnd( Pos ):
					print( "%s %s" % (Pos, "hier ist eine Sackgasse") )
					#try next neighbour
					continue
				if isKnownRoute( Pos ):
					print( "%s %s" % (Pos, "den weg kenne ich schon") )
					#try next neighbour
					continue
				
				print( "%s %s" % (Pos, "vielleicht geht es ja hier weiter?") )
				newWays.append( Pos )
		# add possible ways to visited route
		route.append( newWays )
		printRoute( route )

	print( "hier gehts nicht weiter!" )

if __name__ == "__main__":
	#fileName = "TestField1.txt"
	fileName = "TestField2.txt"
	#fileName = "TestField3.txt"
	#fileName = "TestField4.txt"
	TestField = ReadField( fileName )
	#PrintField( TestField )
	
	#runTests( TestField )
	
	findEscape( TestField, 1, 1 )
	'''
	print( "\n\n\n\n\n" )
	min = 0
	for i in range( 1, len(gefundeneRouten) ):
		if gefundeneRouten[i][0] < gefundeneRouten[min][0]:
			min = i

	print( "Kuerzeste Route hat %d Schritte" % gefundeneRouten[min][0] )
	print( gefundeneRouten[min][1] )
	
	for len,route in gefundeneRouten:
		print( "**********************************" )
		print( "len=%d" % len )
		print( route )
	'''
	#print( "--------------------" )
	#findEscape( TestField, 7, 1 )
	#print( "--------------------" ) 
	#findEscape( TestField, 7, 3 )
	#print( "--------------------" ) 
	#findEscape( TestField, 3, 4 )
