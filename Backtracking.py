#!/usr/bin/python
# -*- coding: UTF-8 -*-

from FloodFill import StripLineEnd, ReadField, PrintField
from FloodFill import emptyMarker, filledMarker, specialMarker, EscapeMarker
import numpy as np
import copy
import os

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

#
def visited( route, pos ):
	for row in route:
		#if pos in row[0]:#geht nicht
		if pos == row[0]:
			return True
	return False

#
def isDeadEnd( pos ):
	global DeadEnds
	#print( "DeadEnds", DeadEnds)
	if pos in DeadEnds:
		return True
	return False

#
def isKnownRoute( pos ):
	global KnownRoute
	#print( "KnownRoute", KnownRoute)
	for route in KnownRoute:
		if pos in route:
			return True
	return False

#
def printRoute( route, text="" ):
	if len(text) > 0:
		print( text )
	for row in route:
		print( row )
def goBack( route ):
	global goBackTimes
	#print("go back call with", "id(route)", id(route))
	Removed = []
	goBackTimes = goBackTimes + 1
	print( "goBackTimes=" ,goBackTimes )
	#i = 0
	#pop last element
	currentPos = route[-1]
	#print( "currentPos", currentPos )
	while len(route) > 1 and ( currentPos == [] or len( currentPos ) == 1 ):
		#i = i + 1
		'''
		if goBackTimes == 10:
			print()
			print("+++++++++++++++")
			print( "currentPos", currentPos )
			print( "len= ", len(route) )
			printRoute( route, "before" )
			print("_______________")
		'''
		if currentPos == []:
			# route kürzen
			#route = route[:-1]
			#del route[:-1]
			route.pop()
			if route:
				currentPos = route[-1]
			#print( "restart go back" )
			#printRoute( route, "after" )
			#continue
		else:
			# zu entfernendes element speichern
			Removed.append( route[-1][:1][0] )
			# Position entfernen
			route[-1] = route[-1][1:]
			#Removed.append( route[-1].pop() )
			currentPos = route[-1]
		
		#print( "currentPos2", currentPos )
		#printRoute( route, "after" )
		#print( "len2=", len(currentPos) )
		#if len(currentPos) > 0:
			#print( currentPos )
		#	break
	Removed.append( route[-1][:1][0] )
	# Position entfernen
	route[-1] = route[-1][1:]
	#Removed.append( route[-1].pop() )
	currentPos = route[-1]
	'''
	print( "2currentPos", currentPos )
	printRoute( route, "route:" )
	printRoute( Removed, "Removed:" )
	print( "Removed2:", Removed )
	'''
	return set( Removed )
	'''
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
	'''

def findEscape( Field, rowNumber, columnNumber, route=[] ):
	global DeadEnds
	global KnownRoute
	global goBackTimes
	KnownRoute = []
	# format (y,x).    >,      <,      ^,     v
	neighbours = ( (0,1), (0,-1), (-1,0), (1,0) )
	Steps = 0
	#DeadEnds = []
#	print( "--------------------" )
#	print( route )
	#print( "z=%d s=%d %s" % (rowNumber, columnNumber, "suche") )

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
			#print( "temp", temp)
			#DeadEnds.append( temp, )
			DeadEnds |= temp
			# doppelte Eintrage entfernen
			#DeadEnds = list( set( DeadEnds ))
			#printRoute(route, "after go back")
			#return
			'''
			if goBackTimes == 10:
				print( "len(route)   = ", len(route) )
				print( "len(route[0])= ", len(route[0]) )
				printRoute( route, "route:" )
			'''
			continue

#		print( "aaa: ", route[-1] )
#		print( "bbb: ", route[-1][0] )
		currentPos = route[-1][0]
		# teste alle Nachbarn
		os.system("clear")
		print( "%s %s" % (currentPos, "--ich bin jetzt hier") )
		drawField = copy.deepcopy( Field )
		for row in route:
			#mark way
			pos = row[0]
			drawField[ pos[0] ][ pos[1] ] = "#"
		for pos in DeadEnds:
			drawField[ pos[0] ][ pos[1] ] = "-"
		
		PrintField( drawField )
		os.system("sleep 0.1")
		
		newWays = []
		for n in neighbours:
			Pos = tuple( np.add( currentPos, n ) )
			# sind wir schon da?
			if isEscape( Field, rowNumber=Pos[0], columnNumber=Pos[1] ):
				# Ausgang gefunden route ausgeben, bzw merken
				print( "%s %s" % (Pos, "Ausgang gefunden") )
				#newRoute = route[:]# ist vielleicht richtig
				newRoute = [ row[0] for row in route ]
				newRoute.append( Pos )
				print( "**********************************************************************" )
				print( "%d Schritte bis zum Ausgang. Diesen Weg muss ich gehen" % len(newRoute) )
				printRoute( newRoute )
				print( "**********************************************************************" )
				#gefundeneRouten.append( newRoute )

				print( "ich schrieb mir mal diesen Weg auf" )
				#KnownRoute = newRoute
				KnownRoute.append( newRoute )
				#goBack( route )
				#break
				'''
				if not KnownRoute:
				# neue kürzere Route gefunden
				elif len(newRoute) < len(KnownRoute):
					# neue Route als beste Route speichern
					print( "habe eine Kürzere Route gefunden")
					KnownRoute = newRoute
					# was ist mit den Punkten, Wegen die länger sind
					# wohin damit
				#return True
				'''
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
		#printRoute( route )
	# while len(route) > 0 :
	print( "fertig meister" )
	print( "%d Route(n) bis zum Ausgang." % len(KnownRoute) )
	for route in KnownRoute:
		drawField = copy.deepcopy( Field )
		for pos in route:
			#mark way
			drawField[ pos[0] ][ pos[1] ] = specialMarker
		
		PrintField( drawField )
	
	# print deadends
	drawField = copy.deepcopy( Field )
	for pos in DeadEnds:
		#mark way
		drawField[ pos[0] ][ pos[1] ] = "-"
	
	PrintField( drawField )
	
	return KnownRoute

if __name__ == "__main__":
	#fileName = "TestField1.txt"
	fileName = "TestField3.txt"
	#fileName = "TestField3.txt"
	#fileName = "TestField4.txt"
	TestField = ReadField( fileName )
	#PrintField( TestField )
	
	#runTests( TestField )
	
	route = findEscape( TestField, 1, 1 )
	#print( "**********************************************************************" )
	#print( "%d Route(n) bis zum Ausgang. Diesen Weg muss ich gehen" % len(route) )
	#printRoute( route )
	#print( "**********************************************************************" )
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
