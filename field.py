#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from FloodFill import StripLineEnd, ReadField, PrintField
from FloodFill import emptyMarker, filledMarker, specialMarker, EscapeMarker
from tkinter import *
import threading
import time
import numpy as np
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

# findEscape stuff
field = None
visitedPoints=[]
posToStartLen = {}

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
	canvas = Canvas( app, width=canvas_width, height=canvas_height, bg="#F0F0F0" )
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
	pad = 5
	x1 = pos1[1] * scale
	y1 = pos1[0] * scale
	x2 = pos2[1] * scale
	y2 = pos2[0] * scale
	nr = canvas.create_line( x1+pad, y1+pad, x2+pad, y2+pad, fill="blue", width=3 )
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
	global canvas_el

	#print( "drawRoute start" )
	#start = time.clock()
	
	# clear previous route
	#for el in canvas_Dot:
	#	canvas.delete( el )
	#for el in canvas_Line:
	#	canvas.delete( el )
	
	canvas.delete( ALL )
	drawField()
	
	#draw lines
	for index in range( len(Route)-1 ):
		drawLine( Route[index], Route[index+1] )
	
	#draw dots
	#for pos in Route:
	#	drawDot( pos )
	
	#end = time.clock()
	#runtime = end - start
	#print( "drawRoute end %f" % runtime )
	pass

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
		if len(route) > Length:
			pass

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

def getNotVisited( Nachbarn, route ):
	res = []
	for FreierNachbar in Nachbarn:
		if not visited(FreierNachbar):
			set_color( 'white' )
			print( FreierNachbar, "frei => hier weitersuchen" )
			res.append( FreierNachbar )
			drawRing( FreierNachbar )
		else:
			teil1 = route[:-2]
			teil2 = route[-2:]
			
			if FreierNachbar in teil2:
				set_color( )
				print( FreierNachbar, "besucht => nicht zurück gehen" )
				#print( "teil1", teil2 )
			
			if FreierNachbar in teil1:
				set_color( 'green' )
				print( FreierNachbar, "besucht => optimieren" )
				# #print( "teil2", teil1 )
				# # TODO: hier route optimieren
				# i = route.index( FreierNachbar )
				# new = route[:i+1]
				# new.append( pos )
				# print( "index:", i, "len %d" % len(new) )
				# if neueRoute == []:
					# neueRoute = new
				# elif len(new) < len(neueRoute):
					# neueRoute = new
	# neueRoute = []
	# if neueRoute != []:
		# print( "Benutze neue Route" )
		# print( "neueRoute", neueRoute )
		# route = neueRoute
		# drawRoute( route )
		# if nichtBesucht == []:
			# return neueRoute

	return res

def getBestRoute( result ):
	bestRoute = []
	
	values = sorted( result.values() )
	for k in values:
		if k != []:
			bestRoute = k
			break
	
	return bestRoute

def findEscape( Field, rowNumber, columnNumber, route=() ):
	global runs
	
	if runs < 0:
		return list()
	
	findEscapeInit( route )
	
	#sync thread
	# wait for runs to be not 0
	sync()
	if runs < 0:
		return list()
	
	# format (y,x).    >,      <,      ^,     v
	richtung = ( (0,1), (0,-1), (-1,0), (1,0) )
	pos = ( rowNumber, columnNumber )
	
	listroute = list( route )
	listroute.append( pos )
	#route = tuple( listroute )
	route = list( listroute )
	drawRoute( route )
	set_color('yellow')
	
	print( "Entry: ", pos )
	print( "Route: %d\n" % len(route), route )
	
	# bin ich am Ausgang
	if isEscape( Field, rowNumber, columnNumber ):
		set_color('green')
		print( pos, "Ausgang gefunden len %d" %len(route) )
		print( route )
		#saveNewRouteToEscape( route )
		set_color()
		return list(route)
	
	# mark this pos as used
	visit( pos, route )
	
	# wenn ich nicht am Ausgang bin,
	# Freie Nachbarn bestimmen (isFree benutzen)
	Nachbarn = []
	for n in richtung:
		temp = tuple( np.add( (rowNumber, columnNumber), n ) )
		if isFree( Field, temp[0], temp[1] ):
			Nachbarn.append( temp )
	
	set_color( 'cyan' )
	print( "Nachbarn", Nachbarn )
	
	# habe alle freien Nachbarn
	# jetzt überprüfe ich, ob einer der Nachbarn schon besucht wurde
	nichtBesucht = getNotVisited( Nachbarn, route )
	
	result = {}
	set_color()
	# hier die nicht besuchten Punkte abarbeiten
	for notvisitedPos in nichtBesucht:
		# Da wir eine rekursion haben, mussen wir überprüfen,
		# ob wir diesen Punkt nicht schon über einen anderen Punkt erreicht haben
		if not visited(notvisitedPos):
			temp = findEscape( Field, notvisitedPos[0], notvisitedPos[1], route )
			result[notvisitedPos] = temp
			print( "zurück nach", pos, len(temp) )
			if pos == (13, 8):
				print( "result\n", result )
			#if temp != None:
			#	# bessere Route bekommen
			#	sync()
			#	drawRoute( route )
		else:
			set_color( 'red' )
			print( notvisitedPos, "dieser Punkt wurde schon besucht" )
			set_color()
			result[notvisitedPos] = []
	
	if pos == (13, 8):
		print( "result\n", result )
	
	best = getBestRoute( result )
	#print( "best", best )
	
	print( pos, "best (%d):" %len(best) )
	#if result != [] and pos == result[0]:
	if best != [] and pos == best[0]:
		set_color('green')
		print( "#######################################################" )
		print( "# Ausgang gefunden :)                                 #" )
		print( "#######################################################" )
		print( best )
		drawRoute( best )
	
	return best

if __name__ == "__main__":
	set_color()
	#fileName = "TestField1.txt"		#spirale
	#fileName = "TestField2.txt"		#klein
	fileName = "TestField4.txt"		#mittel
	#fileName = "TestField3.txt"		#groß
	
	TestField = ReadField( fileName )

	init( TestField )
	'''
		route = [ (1,1), (2,1), (2,2), (3,2), (4,2), (5,2) ]
		#print( route )
		
		drawRoute( route )
		drawRing( (4,1) )
		drawRing( (5,1) )
		drawRing( (6,2) )
	'''
	
	con = threading.Condition()
	
	findEscapeThread = threading.Thread( target = findEscape, args=(TestField, 1, 1) )
	findEscapeThread.start()
	
	
	#route = [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)]
	#drawRoute(route)
	
	app.mainloop()
	
	print( "kill findEscapeThread" )
	# kill findEscapeThread
	con.acquire()
	runs = -1
	con.notify()
	con.release()
	findEscapeThread.join()
	set_color()
