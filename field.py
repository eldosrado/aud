#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from FloodFill import StripLineEnd, ReadField, PrintField
from FloodFill import emptyMarker, filledMarker, specialMarker, EscapeMarker
from tkinter import *
import threading
import time
import numpy as np
import colorsys
#import pandas as pd

try:
	from color_console import set_color
except:
	import colorama
	colorama.init()
	
	def set_color( color='gray' ):
		if color == 'black':
			print( colorama.Fore.BLACK, end='' )
		
		if color == 'blue':
			print( colorama.Fore.BLUE + colorama.Style.BRIGHT , end='' )
			
		if color == 'green':
			print( colorama.Fore.GREEN + colorama.Style.BRIGHT, end='' )
			
		if color == 'cyan':
			print( colorama.Fore.CYAN + colorama.Style.BRIGHT, end='' )
			
		if color == 'red':
			print( colorama.Fore.RED + colorama.Style.BRIGHT, end='' )
			
		if color == 'yellow':
			print( colorama.Fore.YELLOW + colorama.Style.BRIGHT, end='' )
			
		if color == 'magenta':
			print( colorama.Fore.MAGENTA + colorama.Style.BRIGHT, end='' )
			
		if color == 'gray':
			print( colorama.Fore.RESET + colorama.Style.NORMAL, end='' )
			
		if color == 'white':
			print( colorama.Fore.WHITE + colorama.Style.BRIGHT, end='' )

# GUI stuff
app = None
canvas = None
scale = 10

canvas_Rectangle = []
canvas_Line = []
canvas_Dot = []
canvas_LittleDot = []
canvas_Ring = []

input = None
label = None
# sync stuff
con = None
runs = 1
# gui color stuff
LastColor = None
CurrentColor = None


# findEscape stuff
field = None
visitedPoints=[]
DistToStart = {}
isRouteFound = False
#findEscape_runs = 0
#run = False
#Exit = False
def testcolors():
	set_color('blue')
	print( "blue" )
	
	set_color('green')
	print( "green" )
	
	set_color('cyan')
	print( "cyan" )
	
	set_color('red')
	print( "red" )
	
	set_color('yellow')
	print( "yellow" )
	
	set_color('magenta')
	print( "magenta" )
	
	set_color('gray')
	print( "gray" )
	
	set_color('white')
	print( "white" )

def SetRunTime():
	global runs
	global input
	global label
	global con
	
	try:
		intvalue = int( input.get() )
		
		#sync with find thread
		con.acquire()
		
		runs = intvalue
		label.config( text= "will go %d steps" % runs )
		print( "will execute next %d steps" % runs )
		
		con.notify()
		con.release()
		
	except:
		# Fehler ausgeben
		label.config( text="Fehler! Eingabe ist keine Zahl" )

def StopFind():
	global con
	global runs
	
	con.acquire()
	runs = -1
	con.notify()
	con.release()

def init( Field ):
	global app
	global canvas
	global field
	global input
	global label
	
	field = Field
	
	app = Tk()
	
	# create field in canvas
	canvas_width  = len( field[0] ) * scale
	canvas_height = len( field )    * scale
	canvas = Canvas( app, width=canvas_width, height=canvas_height, bg="#000000" )
	canvas.pack( side=TOP, padx=5, pady=5 )
	drawField()
	
	# create next button
	nextbutton = Button( app, text="Next", command=SetRunTime )
	#nextbutton.pack( side=LEFT, padx=5, pady=5 )
	nextbutton.grid( row=0, column=0 )
	nextbutton.pack( side=LEFT, padx=5, pady=5 )
	
	# input for next steps
	input = Entry( app )
	input.grid(row=0, column=1)
	input.pack( side=LEFT, padx=5, pady=5 )
	# preload with valid value
	input.insert( 0, "1" )
	
	#label für ausgaben
	label = Label( app, text=":)" )
	label.grid(row=0, column=2 )
	label.pack( side=LEFT, padx=5, pady=5 )

	#exit button
	exitbutton = Button( app, text="Stop", command=StopFind )
	#nextbutton.pack( side=LEFT, padx=5, pady=5 )
	exitbutton.grid( row=0, column=3 )
	exitbutton.pack( side=LEFT, padx=5, pady=5 )

def SetNewRouteColor():
	global CurrentColor
	global canvas_Line
	
	canvas_Line = []
	CurrentColor = None
	drawRoute.lastRoute = []

def RGBToHTMLColor( rgb_tuple ):
	""" convert an (R, G, B) tuple to #RRGGBB """
	hexcolor = '#%02x%02x%02x' % tuple( rgb_tuple )
	# that's it! '%02x' means zero-padded, 2-digit hex values
	return hexcolor

def GetColor():
	global LastColor
	global CurrentColor
	set_color('blue')
	if LastColor == None:
		#print( "LastColor = None" )
		color = 1.0
		# Farbwert = 100%
		# Sättigung 100%
		# Hellwert = 100%
		LastColor = color
	
	if CurrentColor == None:
		#print( "CurrentColor = None" )
		color = LastColor
		# Farbwert = -10%
		# Sättigung 100%
		# Hellwert = 100%
		sub = 19.0/100.0
		color = color - sub
		if color < 0:
			color = color + 1.0
		
		val = colorsys.hsv_to_rgb( color, 1.0, 1.0 )
		LastColor = color
		
		val2 = [ int( el * 255 ) for el in val ]
		hexcolor = RGBToHTMLColor( val2 )
		
		CurrentColor = hexcolor
		#print( "CurrentColor = %s" % CurrentColor )
	
	set_color()
	return CurrentColor

def drawField( ):
	pad = 2
	for y in range( len(field) ):
		for x in range( len(field[0]) ):
			x1 = x * scale
			y1 = y * scale
			if field[y][x] == filledMarker:
				nr = canvas.create_rectangle( x1+pad, y1+pad, x1 + scale-pad, y1 + scale-pad, fill="yellow" )
				canvas_Rectangle.append( nr )
			if field[y][x] == EscapeMarker:
				canvas.create_rectangle( x1+pad, y1+pad, x1 + scale-pad, y1 + scale-pad, fill="red" )
				canvas_Rectangle.append( nr )

def drawLine( pos1, pos2 ):
	FillColor = GetColor()
	pad = 5
	x1 = pos1[1] * scale
	y1 = pos1[0] * scale
	x2 = pos2[1] * scale
	y2 = pos2[0] * scale
	nr = canvas.create_line( x1+pad, y1+pad, x2+pad, y2+pad, fill=FillColor, width=3 )
	canvas_Line.append( nr )

def drawDot( pos ):
	pad = 2
	x1 = pos[1] * scale
	y1 = pos[0] * scale
	nr = canvas.create_oval( x1+pad, y1+pad, x1 + scale-pad, y1 + scale-pad, fill="blue" )
	canvas_Dot.append( nr )

def drawLittleDot( pos ):
	pad = 4
	x1 = pos[1] * scale
	y1 = pos[0] * scale
	nr = canvas.create_oval( x1+pad, y1+pad, x1 + scale-pad, y1 + scale-pad, fill="blue" )
	canvas_LittleDot.append( nr )

def drawRing( pos ):
	#pad = 2
	#x1 = pos[1] * scale
	#y1 = pos[0] * scale
	#nr = canvas.create_oval( x1+pad, y1+pad, x1 + scale-pad, y1 + scale-pad, fill="" )
	#canvas_Ring.append( nr )
	pass

def drawRoute( Route ):
	if not hasattr( drawRoute, "lastRoute" ):
		lastRoute = drawRoute.lastRoute = []
	else:
		lastRoute = drawRoute.lastRoute
	
	global canvas_el
	
	start = time.clock()
	DrawIndex = 0
	# clear previous route

	lenRoute     = len(Route)
	lenlastRoute = len(lastRoute)
	
	# if new route is longer, we go probaly the same way
	# if not, draw a new route
	if lenlastRoute < lenRoute:
		print( lenlastRoute, "<", lenRoute )
		for index in range( len(lastRoute) ):
			if lastRoute[index] == Route[index]:
				DrawIndex = index
				continue
			canvas.delete(index)
	else:
		print( lenlastRoute, ">=", lenRoute )
		SetNewRouteColor()
	
	
	#draw lines
	print( DrawIndex, len(Route)-1, len(Route)-1-DrawIndex )
	for index in range( DrawIndex, len(Route)-1 ):
	#for index in range( len(Route)-1 ):
		drawLine( Route[index], Route[index+1] )
	
	#lastRoute = list( Route )
	#del lastRoute[:]
	#lastRoute.extend( Route )
	drawRoute.lastRoute = list( Route )
	#draw dots
	#for pos in Route:
	#	drawDot( pos )
	
	print( "drawRoute 3 runtime %f" % (time.clock() - start) )

def sync():
	global con
	global runs

	con.acquire()
	while runs == 0:
		print( "findEscape is waiting\n" )
		con.wait()
	#print( "findEscape is running" )
	runs -= 1
	con.release()

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
	if Field[rowNumber][columnNumber] == filledMarker:
		return False
	return True

def isEscape( Field, rowNumber, columnNumber ):
	if not inField( Field, rowNumber, columnNumber ):
		return False
	if Field[rowNumber][columnNumber] != EscapeMarker:
		return False
	return True

def visit( pos, route=[] ):
	global visitedPoints
	#global posToStartLen
	
	if not pos in visitedPoints:
		'''
		Wenn pos noch nicht besucht wurde, die aktuelle länge der Route und die Route speichern
		'''
		visitedPoints.append( pos )
		Length = len(route)
		posToStartLen[ pos ] = len(route)
	else:
		Length = posToStartLen[ pos ]
		if len(route) < Length:
			print("visit(): got better route")

def visited( pos ):
	global visitedPoints
	if pos in visitedPoints:
		return True
	return False

def findEscapeInit( route ):
	global visitedPoints
	
	if len(route) == 0:
		print( "Init findEscape" )
		visitedPoints = []
		posToStartLen = []

def getNeighbors( Field, Pos, LastPos ):
	
	Nachbarn = []
	#format      (y,x)    >,      <,      ^,      v
	richtung = (      (0,1), (0,-1), (-1,0),  (1,0) )
	for n in richtung:
		temp = tuple( np.add( Pos, n ) )
		if isFree( Field, temp[0], temp[1] ) and temp not in LastPos:
			Nachbarn.append( temp )
	return Nachbarn

def getNotVisited( Nachbarn, route ):
	res = []
	CurrentPos = route[-1:]
	LastPos    = route[-2:-1]
	print( "CurrentPos", CurrentPos )
	print( "LastPos", LastPos )
	RouteLen = len( route )
	for FreierNachbar in Nachbarn:
		
		
		if FreierNachbar in DistToStart:
			#print( FreierNachbar, "is in DistToStart" )
			PosLen = DistToStart[ FreierNachbar ]
			
			if RouteLen < PosLen:
				print( FreierNachbar, "PosLen (", PosLen,") < ", "RouteLen(", RouteLen , ")" , "=> hier weiter suchen")
				res.append( FreierNachbar )
			else:
				print( FreierNachbar, "PosLen (", PosLen,") => ", "RouteLen(", RouteLen , ")", "=> nicht zurück gehen" )
			
		else:
			print( FreierNachbar, "ist noch UNbesucht!" )
			res.append( FreierNachbar )
		
		
		
		'''
		if FreierNachbar in LastPos:
			print( FreierNachbar, "besucht (Last) => nicht zurück gehen" )
		elif FreierNachbar in route:
			print( FreierNachbar, "besucht (route)=> nicht zurück gehen" )
		#elif FreierNachbar in DistToStart:
		else:
			#if (25, 64) in CurrentPos:
			#	printDistToStart()
			# erstmal ein paar sachen ausgeben
			print( FreierNachbar, "frei           => hier weitersuchen" )
			res.append( FreierNachbar )
		# elif not visited(FreierNachbar):
			# set_color( 'white' )
			# print( FreierNachbar, "frei => hier weitersuchen" )
			# res.append( FreierNachbar )
			# drawRing( FreierNachbar )
		'''
			
			
			
			
		# else:
			# teil1 = route[:-2]
			# teil2 = route[-2:]
			
			# if FreierNachbar in teil2:
				# set_color( )
				# print( FreierNachbar, "besucht => nicht zurück gehen" )
				# #print( "teil1", teil2 )
			
			# if FreierNachbar in teil1:
				# set_color( 'green' )
				# print( FreierNachbar, "besucht => optimieren" )
	print( "" )
	return res

def isBetterRoute( pos, Nachbarn, route ):
	#print( "drawRoute start" )
	start = time.clock()
	
	teil1 = route[:-2]
	teil2 = route[-2:]
	neueRoute = []
	
	for FreierNachbar in Nachbarn:
		
		# if FreierNachbar in teil2:
			# set_color( )
			# print( FreierNachbar, "besucht => nicht zurück gehen" )
			# #print( "teil1", teil2 )
		
		# else:
		if FreierNachbar in teil1:
			set_color( 'green' )
			print( FreierNachbar, "besucht => optimieren" )
			print( "route", route )
			
			#print( "teil2", teil1 )
			# TODO: hier route optimieren
			i = route.index( FreierNachbar )
			
			new = route[:i+1]
			new.append( pos )
			print( "new  ", new )
			print( "index:", i, "len %d" % len(new) )
			
			if neueRoute == []:
				neueRoute = new
			elif len(new) < len(neueRoute):
				neueRoute = new
		
	# neueRoute = []
	# if neueRoute != []:
		# print( "Benutze neue Route" )
		# print( "neueRoute", neueRoute )
		# route = neueRoute
		# drawRoute( route )
		# if nichtBesucht == []:
			# return neueRoute
	#end = time.clock()
	#runtime = end - start
	print( "isBetterRoute runtime %f" % (time.clock() - start) )
	return neueRoute

def getBestRoute( result ):
	bestRoute = []
	
	values = list( result.values() )
	values.sort( key = len )
	
	for k in values:
		if k != []:
			bestRoute = k
			break
	
	return bestRoute
'''
def SaveDistToStart( pos, route ):
	print( "SaveDistToStart", pos, "dist", len(route) )
	DistToStart[ pos ] = len( route )
'''
'''
def printDistToStart( ):
	print( "DistToStart" )
	
	#var = DistToStart.items()
	#print( DistToStart )
	#print( var )
	
	#for key, value in DistToStart.items():
	#	print( key, value, ",", end='' )
	#print( "" )
	print( "now with pandas" )
	print( "+++++++++++++++++++" )
	
	data = pd.Series( DistToStart )
	pd.set_option('display.max_rows', len(data))
	print( data[:] )
'''
def isin( pos, result ):
	for myvalue in result.values():
		if pos in list( myvalue ):
			return True
	return False

def findEscape( Field, rowNumber, columnNumber, route=() ):
	# found format| len : route
	if not hasattr( findEscape, "found" ):
		found = findEscape.found = {}
	else:
		found = findEscape.found
	global runs
	if runs < 0:
		return list()
	
	findEscapeInit( route )
	
	#sync thread
	# wait for runs to be not 0
	sync()
	if runs < 0:
		return list()
	
	pos = ( rowNumber, columnNumber )
	
	listroute = list( route )
	listroute.append( pos )
	#route = tuple( listroute )
	route = list( listroute )
	RouteLen = len( route )
	drawRoute( route )
	set_color('yellow')
	print( "route\n",route )
	LastPos = route[-2:-1]
	'''
	if RouteLen > 1:
		LastPos = route[-2:-1]
	else:
		LastPos = pos
	'''
	print( "Entry: ", pos, "LastPos", LastPos )
	
	#print( "Route: %d\n" % len(route), route )
	
	# bin ich am Ausgang
	if isEscape( Field, rowNumber, columnNumber ):
		global isRouteFound
		set_color('green')
		print( pos, "Ausgang gefunden len %d" %len(route) )
		print( route )
		#saveNewRouteToEscape( route )
		set_color()
		isRouteFound = True
		found[RouteLen] = route
		findEscape.found = found
		return list(route)
	
	# mark this pos as used
	#visit( pos, route )
	
	# save distance to start for current position
	set_color( 'green' )
	#SaveDistToStart( pos, route )
	DistToStart[ pos ] = RouteLen
	
	# wenn ich nicht am Ausgang bin,
	# Freie Nachbarn bestimmen (isFree benutzen)
	Nachbarn = getNeighbors( Field, pos, LastPos )
	# remove previous point in route
	'''
	try:
		i = Nachbarn.index( LastPos )
		Nachbarn.pop( i )
	except:
		pass
	'''
	set_color( 'cyan' )
	print( "Nachbarn", Nachbarn )
	
	# habe alle freien Nachbarn
	
	if len(Nachbarn) == 1 and Nachbarn[0] in route[-2:-1]:
		res = -1 * RouteLen
		DistToStart[ pos ] = res
		set_color( 'red' )
		print( "Sackgasste!! res %d" % res )
		set_color( )
		return []

	
	#nichtBesucht = getNotVisited( Nachbarn, route )
	'''
	BetterRoute = isBetterRoute( pos, Nachbarn, route )
	if BetterRoute != []:
		#print( BetterRoute )
		print( "there is a better Route!!!!" )
	'''
	result = {}
	set_color()
	best = []
	# hier die nicht besuchten Punkte abarbeiten
	for unvisitedPos in Nachbarn:
		# Da wir eine rekursion haben, muss immer überprüft werden,
		# ob dieser Punkt nicht schon über einen anderen Punkt erreicht wurde.
		# Und wenn doch, dann kann der Punkt nur nochmal überprüft werden,
		# wenn der aktuelle Weg zu diesem Punkt kürzer war
		temp = []
		# unvisited Positionen müssen immer untersucht werden!!! Egal Was
		if not unvisitedPos in DistToStart:
			print( unvisitedPos, "ist noch UNbesucht!" )
			temp = findEscape( Field, unvisitedPos[0], unvisitedPos[1], route )
			print( "zurück nach", pos, len(temp) )
			result[unvisitedPos] = temp
		
		else:# unvisitedPos in DistToStart:
			PosLen = DistToStart[ unvisitedPos ]
			
			# Solange wir keinen Ausgang kennen, lassen wir alle schon besuchten Punkte aus.
			# Da diese offensichtlich nicht zum Ausgang führen
			if isRouteFound == False:
				print( unvisitedPos, "kein Weg zum Ausgang bekannt => auslassen!!" )
				pass
			else:
				# Wenn wir einen Weg zum Ausgang kennen, dann untersuchen wir nur Punkte
				# wo die aktuelle Länge der Route kleiner ist als
				# die vorherige Länge zu diesem Punkt.
				# Und wir lassen alle Punkte aus, die in dem Weg zum Ausgang sind.
				
				# Dann machen wir das mal.
				# als Erstes überprüfen wir die Länge
				if RouteLen < PosLen:
					# So die Länge ist größer als unsere Route
					# Dann müssen wir Überprüfen, ob dieser Punkt im Ausgangsweg ist
					#if not isin( unvisitedPos, result ):
					if not isin( unvisitedPos, found ):
						# Dieser Punkt ist nicht im Ausgangsweg
						'''
						Das funktioniert nicht so wie es jetzt ist.
						Wenn ich einen Seitenroute auswähle und nur mit der Route starte,
						kenn diese nicht den Weg zum Ausgang!!!
						Das heißt die nächste Instanz sucht und sucht und sucht.
						Dabei werden zwar immer bessere Weg zum Ausgang gefunden, aber das Dauert!!!
						
						Ich muss also entweder global den Weg zum Ausgang bereitstellen,
						oder es als Route übergeben
						oder einen zusätzlichen Parameter zur funktuion hinzufügen
						oder eine Statische Variable. <--
						'''
						print( unvisitedPos, "is not in" )
						print( found )
						print( unvisitedPos, "RouteLen  < PosLen ", RouteLen , " <", PosLen, "=> hier weiter suchen")
						temp = findEscape( Field, unvisitedPos[0], unvisitedPos[1], route )
						print( "zurück nach", pos, len(temp) )
						result[unvisitedPos] = temp
					
				else:
					# Wenn dieser Punkt schon mal besucht wurde, muss überprüft werden,
					# ob der aktuelle Weg im "Kreis" gegangen ist.
					print( unvisitedPos, "RouteLen >= PosLen ", RouteLen , ">=", PosLen, "=> nicht zurück gehen" )
					# if unvisitedPos in route[:-2]:
						# print( "im kreis gegangen" )
						# # markieren ob wir im Kreis gegangen sind
						# result[unvisitedPos] = unvisitedPos
	
	best = getBestRoute( result )
	print( "best", best )
	print( pos, "best (%d):" %len(best) )
	
	# if nothing is found, mark this pos as do not visit again
	if isRouteFound == True:
		if len(best) == 0:
			res = -1 * RouteLen
			DistToStart[ pos ] = res
			print( "res %d" % res )
	
	if best != [] and isinstance( best, list ) and pos == best[0]:
		set_color('green')
		print( "#######################################################" )
		print( "# Ausgang gefunden :)                                 #" )
		print( "#######################################################" )
		print( best )
		SetNewRouteColor()
		drawRoute( best )
	
	return best

if __name__ == "__main__":
	#drawRoute.lastRoute = []
	
	debug = False
	set_color()
	#fileName = "TestField1.txt"		#spirale
	#fileName = "TestField2.txt"		#klein
	#fileName = "TestField4.txt"		#mittel
	fileName = "TestField3.txt"		#groß
	
	TestField = ReadField( fileName )
	init( TestField )
	
	if debug == True:
		for i in range( 20 ):
			route = [ (i,1), (i,2) ]
			drawRoute( route )
		
		app.mainloop()
		exit()
	
	con = threading.Condition()
	
	findEscapeThread = threading.Thread( target = findEscape, args=(TestField, 1, 1) )
	findEscapeThread.start()
	
	
	#route = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)]
	#drawRoute(route)
	
	app.mainloop()
	#printDistToStart()
	
	print( "kill findEscapeThread" )
	# kill findEscapeThread
	con.acquire()
	runs = -1
	con.notify()
	con.release()
	findEscapeThread.join()
	set_color()
