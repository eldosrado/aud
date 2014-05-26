#!/usr/bin/python
# -*- coding: UTF-8 -*-

from FloodFill import StripLineEnd, ReadField, PrintField
from FloodFill import emptyMarker, filledMarker, specialMarker, EscapeMarker
import numpy as np
import copy
import os
import time

goBackTimes = 0
#DeadEnds = []
DeadEnds = set()
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
	global DeadEnds
	#print( "DeadEnds", DeadEnds)
	if pos in DeadEnds:
		return True
	return False

def isKnownRoute( pos ):
	global KnownRoute
	#print( "KnownRoute", KnownRoute)
	for route in KnownRoute:
		if pos in route:
			return True
	return False

def printRoute( Field, route, DeadEnds ):
	Field = copy.deepcopy( Field )
	
	for row in route:
		#mark way
		pos = row[0]
		Field[ pos[0] ][ pos[1] ] = "#"
	for pos in DeadEnds:
		Field[ pos[0] ][ pos[1] ] = "-"
		
	if os.name == "nt":
		os.system( "cls" )
	else:
		os.system( "clear" )
	PrintField( Field )
	'''
	if os.name != "nt":
		os.system("sleep 0.1")
	else:
		time.sleep( 0.01)
	'''

def goBack( route ):
	#global goBackTimes
	#print("go back call with", "id(route)", id(route))
	Removed = []
	#goBackTimes = goBackTimes + 1
	#print( "goBackTimes=" ,goBackTimes )
	#pop last element
	currentPos = route[-1]
	while len(route) > 1 and ( currentPos == [] or len( currentPos ) == 1 ):
		if currentPos == []:
			# route kürzen
			route.pop()
			if route:
				currentPos = route[-1]
		else:
			# zu entfernendes element speichern
			Removed.append( route[-1][:1][0] )
			# Position entfernen
			route[-1] = route[-1][1:]
			currentPos = route[-1]
		
	Removed.append( route[-1][:1][0] )
	# Position entfernen
	route[-1] = route[-1][1:]
	currentPos = route[-1]
	return set( Removed )

def findEscape( Field, rowNumber, columnNumber, route=[] ):
	global DeadEnds
	global KnownRoute
	KnownRoute = []
	# format (y,x).    >,      <,      ^,     v
	neighbours = ( (0,1), (0,-1), (-1,0), (1,0) )
	Steps = 0

	if len(route) == 0 :
		route.append( [(rowNumber,columnNumber)] )
	currentPos = route[-1][0]
	PrintField( Field )
	print( "%s %s" % (currentPos, "Hallo ich bin Lara und ich muss jetzt durch dieses Labyrinth") )
	
	while len(route) > 0 and len(route[0]) > 0:
		# TODO: remove Steps. Only needed for debugging
		'''
		Steps = Steps + 1
		if Steps > 50000:
			return
		'''
		
		# teste, ob wir in einer Sackgasse stecken
		if route[-1] == []:
			print("hmm eine Sackgasse. muss ich wohl zurück" )
			temp = goBack( route )
			DeadEnds |= temp
			continue

		currentPos = route[-1][0]
		print( "%s %s" % (currentPos, "--ich bin jetzt hier") )
		printRoute( Field, route, DeadEnds )
		
		newWays = []
		for n in neighbours:
			Pos = tuple( np.add( currentPos, n ) )
			# sind wir schon da?
			if isEscape( Field, rowNumber=Pos[0], columnNumber=Pos[1] ):
				# Ausgang gefunden route ausgeben, bzw merken
				print( "%s %s" % (Pos, "Ausgang gefunden") )
				newRoute = [ row[0] for row in route ]
				newRoute.append( Pos )
				print( "**********************************************************************" )
				print( "%d Schritte bis zum Ausgang. Diesen Weg muss ich gehen" % len(newRoute) )
				print( "**********************************************************************" )
				
				print( "ich schrieb mir mal diesen Weg auf" )
				KnownRoute.append( newRoute )
			
			# ist nachbar frei
			elif isFree( Field, rowNumber=Pos[0], columnNumber=Pos[1] ):
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

	print( "fertig meister" )
	print( "%d Route(n) bis zum Ausgang." % len(KnownRoute) )
	for route in KnownRoute:
		drawField = copy.deepcopy( Field )
		for pos in route:
			#mark way
			drawField[ pos[0] ][ pos[1] ] = specialMarker
		
		PrintField( drawField )
	
	# print deadends
	'''
	drawField = copy.deepcopy( Field )
	for pos in DeadEnds:
		#mark way
		drawField[ pos[0] ][ pos[1] ] = "-"
	
	PrintField( drawField )
	'''
	return KnownRoute

if __name__ == "__main__":
	#fileName = "TestField1.txt"		#spirale
	#fileName = "TestField2.txt"		#klein
	fileName = "TestField3.txt"		#groß
	#fileName = "TestField4.txt"		#mittel
	
	TestField = ReadField( fileName )
	#PrintField( TestField )
	
	
	route = findEscape( TestField, 1, 1 )
