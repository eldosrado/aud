#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from FloodFill import StripLineEnd, ReadField, PrintField
from FloodFill import emptyMarker, filledMarker, specialMarker, EscapeMarker
from tkinter import *
import threading
import time
import numpy as np
import colorsys
import terminalsize

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
DistToStart  = {}
DistToEscape = {}
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
	input.insert( 0, "1404" )
	
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
		if isRouteFound == False:
			val = colorsys.hsv_to_rgb( color, 0.75, 1.0 )
		else:
			val = colorsys.hsv_to_rgb( color, 1.0, 1.0 )
		LastColor = color
		
		val2 = [ int( el * 255 ) for el in val ]
		hexcolor = RGBToHTMLColor( val2 )
		
		CurrentColor = hexcolor
		#print( "CurrentColor = %s" % CurrentColor )
	
	set_color()
	return CurrentColor

def drawField( ):
	canvas.delete( ALL )
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
		#print( lenlastRoute, "<", lenRoute )
		for index in range( len(lastRoute) ):
			if lastRoute[index] == Route[index]:
				DrawIndex = index
				continue
			canvas.delete(index)
	else:
		#print( lenlastRoute, ">=", lenRoute )
		SetNewRouteColor()
	
	
	#draw lines
	#print( DrawIndex, len(Route)-1, len(Route)-1-DrawIndex )
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
	
	#print( "drawRoute 3 runtime %f" % (time.clock() - start) )
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

def inField( Field, pos ):
	rowNumber    = pos[0]
	columnNumber = pos[1]

	LeftBorder = 0
	RightBorder = len(Field[0])-1
	TopBorder = 0
	BottomBorder = len( Field )-1
	if columnNumber < LeftBorder or columnNumber > RightBorder or \
			rowNumber < TopBorder or rowNumber > BottomBorder:
		return False
	return True

def isFree( Field, pos ):
	rowNumber    = pos[0]
	columnNumber = pos[1]

	if not inField( Field, pos ):
		return False
	if Field[rowNumber][columnNumber] == filledMarker:
		return False
	return True

def isEscape( Field, pos ):
	rowNumber    = pos[0]
	columnNumber = pos[1]
	
	if not inField( Field, pos ):
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
		tempPos = tuple( np.add( Pos, n ) )
		if isFree( Field, tempPos ) and tempPos not in LastPos:
			Nachbarn.append( tempPos )
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
def isin( pos, found ):
	for value in found.values():
		if pos in list( value ):
			return True
	return False

def getFound( pos, found ):
	for value in found.values():
		tmpList = list( value )
		if pos in tmpList:
			return tmpList

# route
# found
# RouteLen ^= Index of currentPos in Route
# unvisitedPosIndex ^= Index of Next in found
#   NeuerWegZumAusgang( route, found, RouteLen, unvisitedPosIndex )
def NeuerWegZumAusgang( route, found, RouteLen, unvisitedPosIndex ):
	set_color( 'yellow' )
	print( "Bestimme neuen Weg zum Ausgang!" )
	#print( "next", unvisitedPos, "current", pos )
	print( "route" );print( route, "\n" )
	print( "found" );print( found, "\n" )
	
	print( "\nRouteLen", RouteLen, "len(route)", len(route), "len(found)", len(found) )
	# Finde gemeinsamen Punkt von route und found
	# Vom Ende aus.
	commonPointIndex = RouteLen - 1
	while route[commonPointIndex] != found[commonPointIndex]:
		print( "i", commonPointIndex, route[commonPointIndex], found[commonPointIndex] )
		commonPointIndex -= 1
	print( "i", commonPointIndex, route[commonPointIndex], found[commonPointIndex] )
	# Der neue Weg setzt sich zusammen aus:
	# Von s bis unvisitedPosIndex von found
	# Von currentPos bis commonPointIndex von route (also Rückwärts)
	# Von commonPointIndex bis E von found
	
	partA = found[ : unvisitedPosIndex+1 ]
	partB = route[ : commonPointIndex : -1 ]
	partC = found[ commonPointIndex: ]
	
	print( "Neuer Weg:\n" )
	
	print( "\nPart A len %d" %len(partA)  )
	print( partA )
	
	print( "\nPart B len %d" %len(partB)  )
	print( partB )
	
	print( "\nPart C len %d" %len(partC)  )
	print( partC )
	
	new = []
	new.extend( partA )
	new.extend( partB )
	new.extend( partC )
	
	print( "\nnew len %d" %len(new)  )
	print( new )
	
	return new
	pass

def getCurrentRoute( PreviousRoute, CurrenPos ):
	"""
	"""
	NewRoute = list( PreviousRoute )
	NewRoute.append( CurrenPos )
	
	return NewRoute
	listroute = list( route )
	listroute.append( pos )
	#route = tuple( listroute )
	route = list( listroute )

def SaveDistToEscape( pos, temp ):
	try:
		DistToEscape[ pos ] = min( DistToEscape[ pos ], temp )
		#if pos in DistToEscape:
		#	DistToEscape[ pos ] = min( DistToEscape[ pos ] or float("inf"), temp )
		#else:
		#	DistToEscape[ pos ] = temp or float("inf")
	except:
		print( "###################################################################" )
		print( pos, temp )
		if pos in DistToEscape:
			print( DistToEscape[ pos ] )
		raise

def findEscape( Field, pos=(1,1), PreviousRoute=() ):
	"""
	Call this function with a field to search in.
	Use ReadField( fileName ) to get a proper field.
	
	returning a list of tuple with the best route to Escape.
	
	Internal::
	returning distance to Escape
	"""
	
	if not hasattr( findEscape, "found" ):
		found = findEscape.found = []
		findEscape.first = pos
	else:
		found = findEscape.found
	global runs
	
	findEscapeInit( PreviousRoute )
	
	# Sync with GUI-Thread
	# Wait for runs to be not 0
	# For debugging purposses, all instances will exit if runs is < 0
	if runs < 0:
		return None
	sync()
	if runs < 0:
		return None
	
	route = getCurrentRoute( PreviousRoute, pos )
	RouteLen = len( route )
	drawRoute( route )
	LastPos = route[-2:-1]
	
	set_color('yellow')
	print( pos, "LastPos", LastPos )
	#print( "route\n",route )
	#print( "Route: %d\n" % len(route), route )
	set_color()
	
	if pos not in DistToEscape:
		DistToEscape[pos] = float("inf")
	
	#####################################################################################
	"""
	Trivialer Fall bei einer Rekursion.
	
	Hier: Ein Ausgang gefunden wurde gefunden
	Wenn das passiert, wird der Weg zum Ausgang als Attribut in diese Funktion gespeichert.
	Damit haben alle Instanzen Zugriff auf diesen Weg.
	
	Hinweis: Wenn eine andere Instanz einen kürzeren Weg zum Ausgang findet,
	wird dieser neue Weg gespeichert!
	"""
	if isEscape( Field, pos ):
		global isRouteFound
		isRouteFound = True
		
		set_color('green')
		print( pos, "Ausgang gefunden len %d" %len(route) )
		print( route )
		set_color()
		
		# TODO 1.1 Den Weg zum Ausgang auf die kürzest möglichen Weg reduzieren
		findEscape.found = route
		SaveDistToEscape( pos, 1 )
		#DistToEscape[ pos ] = 1
		return DistToEscape[ pos ]
	
	#####################################################################################
	"""
	Nicht trivialer Fall der Rekursion
	
	Die aktuelle Position ist nicht der Ausgang.
	Es müssen alle direkten Nachbar untersucht werden, ob nicht diese zum Ausgang führen.
	"""
	Nachbarn = getNeighbors( Field, pos, LastPos )
	
	#####################################################################################
	"""
	Von nun an muss unterschieden werden ob ein Ausgang gefunden wurde oder nicht.
	
	Für den Fall, dass noch kein Weg gefunden wurde, dann wird für diese Position die 
	Entfernung zum Start der Suche eingetragen. Wenn eine andere Instanz wieder zu 
	dieser Position gelangt, wird nicht weiter gesucht. 
	Das verhindert das wiederholte Suchen in Sackgassen!
	"""
	
	if isRouteFound == False:
		DistToStart[ pos ] = RouteLen
		print( pos, "Dist to Start", RouteLen, "saved" )
	else:
		#DistToStart[ pos ] = RouteLen
		print( pos, "Dist to Start", RouteLen, "saved" )
		"""
		Wenn wir einen Weg zum Ausgang kennen und von einer anderen Instanz aufgerufen 
		wurden, dann hat diese Instanz immer eine Entfernung bis zum Ausgang gespeichert!
		Und diese benutzen wir um für die Aktuelle Position die Distanz zu speichern!
		"""
		print( pos, "LastPos", LastPos )
		LastPosTuple = LastPos[0]
		#print( pos, "LastPosTuple", LastPosTuple )
		DistToEscape_fromPrev = DistToEscape[LastPosTuple]
		print( pos, "DistToEscape_fromPrev", DistToEscape_fromPrev )
		DistToEscape[pos] = DistToEscape_fromPrev + 1
		print( pos, "DistToEscape[pos]", DistToEscape[pos] )
	
	#####################################################################################
	"""
	Nun werden alle direkten Nachbarn untersucht.
	"""
	if isRouteFound == False:
		set_color( 'cyan' )
		print( pos, "Nachbarn1", Nachbarn )
		set_color()
		for unvisitedPos in Nachbarn:
			temp = float("inf")
			#####################################################################################
			"""
			Für den Fall, dass noch kein Weg gefunden wurde.
			
			Dann muss überprüft werden, ob dieser Nachbar nicht durch eine andere Instanz 
			erreicht wurde. Nur wenn das nicht der Fall ist, wird für diesen Nachbarn eine 
			neue Suche gestartet
			"""
			if not unvisitedPos in DistToStart:
				print( pos, ">>", unvisitedPos )
				temp = findEscape( Field, unvisitedPos, route )
				print( pos, "<<", unvisitedPos, temp )
				# Wenn eine Route gefunden wurde, dann den akutell bearbeiteten Nachbarn ertfernen
				if temp < float("inf"):
					SaveDistToEscape( pos, temp+1 )
					Nachbarn.remove( unvisitedPos )
					break
	
	if isRouteFound == True:
		set_color( 'cyan' )
		print( pos, "Nachbarn2", Nachbarn )
		set_color()
		for unvisitedPos in Nachbarn:
			temp = None
			found = findEscape.found
			FoundLen = len( found )
			"""
			Für den Fall, dass ein Weg gefunden wurde, dann:
			"""
			if unvisitedPos in found:
				"""
				Wenn ein Nachbar im Weg zum Ausgang ist, dann gibt es vielleicht einen kürzeren Weg.
				Sollte das so sein, wird der neue bessere Weg gespeichert.
				"""
				if pos in found:
					"""
					Die aktuelle Position und der Nachbar sind im Weg zum Ausgang!
					"""
					#####################################################################################
					set_color( 'blue' )
					print( pos, "possible optimization for", unvisitedPos )
					
					#??? unvisitedPosIndex = DistToEscape[unvisitedPos]
					unvisitedPosIndex = found.index( unvisitedPos )
					currentPosIndex   = found.index( pos )
					#DistToEsc = FoundLen - unvisitedPosIndex
					#NewLen = RouteLen + DistToEsc
					
					print( pos, "RouteLen", RouteLen, "unvisitedPosIndex", unvisitedPosIndex )
					#print( pos, "DistToEsc", DistToEsc, "NewLen", NewLen )
					#print( pos, "FoundLen", FoundLen, "NewLen", NewLen )
					
					if currentPosIndex < unvisitedPosIndex:
						set_color( 'green' )
						print( pos, "found better way over", unvisitedPos, unvisitedPosIndex - currentPosIndex, "shorter" )
						
						new = found[:currentPosIndex+1]
						new.extend( found[unvisitedPosIndex:] )
						findEscape.found = found = new
						# TODO: hier villeicht noch DistToEscape[pos] nachtragen ???
						temp = DistToEscape[unvisitedPos]
						
						print( pos, "new len %d" %len(new) );
						#print( new )
						
						SetNewRouteColor()
						drawRoute( new )
						sync()
					else:
						print( pos, "not a better way over", unvisitedPos, currentPosIndex - unvisitedPosIndex, "longer" )
				else:
					"""
					Die aktuelle Position ist nicht im Weg zum Ausgang!
					Es gibt für die akutelle Position eine Distanz bis zum Ausgang.
					
					Diese Distanz wird zu der Distanz, die der Nachbar zum Start hat addiert.
					Wenn dieser Wert kleiner ist, dann gibt es eine neue Bessere Route zum Ausgang!
					"""
					# S->Next
					unvisitedPosIndex = found.index( unvisitedPos )
					newLen = unvisitedPosIndex + 1 + DistToEscape[pos]
					set_color( 'yellow' )
					
					print( pos, "unvisitedPosIndex", unvisitedPosIndex, "DistToEscape", DistToEscape[pos] )
					print( pos, "newLen", newLen, "FoundLen", FoundLen )
					
					if newLen < FoundLen:
						print( pos, "found better way over", unvisitedPos, FoundLen - newLen, "shorter" )
						# route
						# found
						# RouteLen ^= Index of Pos in Route
						# unvisitedPosIndex ^= Index of Next in found
						new = NeuerWegZumAusgang( route, found, RouteLen, unvisitedPosIndex )
						findEscape.found = found = new
						#prevDistToEscape = DistToEscape[pos]
						#DistToEscape[unvisitedPos] = DistToEscape[pos]+1
						#print( pos, "prevDistToEscape", prevDistToEscape, "newDistToEscape", DistToEscape[pos] )
						SetNewRouteColor()
						drawRoute( new )
						sync()
					else:
						print( pos, "not a better way over", unvisitedPos, newLen - FoundLen , "longer" )
					pass
				set_color()
			elif unvisitedPos in DistToEscape and DistToEscape[unvisitedPos] < DistToEscape[pos]:
				#####################################################################################
				"""
				Wenn ein Nachbar nicht im Weg zum Ausgang ist, aber es ist für diesen Nachbarn schon
				eine Entfernung zum Ausgang angegeben.
				Dann muss überprüft werden, ob es nicht einen kürzeren Weg zum Ausgang über diesen
				Nachbar gibt.
				"""
				set_color( 'cyan' )
				dist = FoundLen - DistToEscape[ unvisitedPos ]
				
				
				if RouteLen + dist < FoundLen:
					print( pos, "possible shorter route over", unvisitedPos, "RouteLen", RouteLen, "+", dist , " <", FoundLen )
				else:
					print( pos, "possible shorter route over", unvisitedPos, "RouteLen", RouteLen, "+", dist , ">=", FoundLen )
				
				set_color()
				pass
			elif unvisitedPos in DistToStart:
				#####################################################################################
				"""
				Nachbar ist nicht im Weg zum Ausgang und
				es ist keine Entfernung zum Ausgang angegeben und
				dieser Nachbar wurde schon besucht.
				???
				Ich will unnötige suchen vermeiden, deshalb erstmal gucken ob die neue route nicht schon länger wäre
				als der Weg zum ausgang
				
				
				
				Wenn dieser Punkt keinen neuen Weg zum Ausgang kennt, dann muss ich diesen Punkt endgültig als Sackgasse markieren.
				Oder ich muss bei der ermittlung des Rückgabewertes noch was machen.
				Es stört eigentlich nicht, dass diese Punkte nochmal und nochmal besucht werden.
				Es kostet halt immer nur Zeit
				???
				"""
				
				if RouteLen + 1 < FoundLen:
					set_color( 'red' )
					print( pos, unvisitedPos, "visited before" )
					print( pos, "RouteLen", RouteLen, "FoundLen", FoundLen, "DistToStart", DistToStart[unvisitedPos] )
					set_color()
					print( pos, ">>", unvisitedPos, DistToEscape[pos] )
					temp = findEscape( Field, unvisitedPos, route )
					print( pos, "<<", unvisitedPos, temp )
				else:
					set_color( 'red' )
					print( pos, "RouteLen > FoundLen" )
					#print( pos, unvisitedPos, "visited before" )
					#print( pos, "RouteLen", RouteLen, "FoundLen", FoundLen, "DistToStart", DistToStart[unvisitedPos] )
					
					set_color()
			else:
				#####################################################################################
				"""
				Nachbar ist nicht im Weg zum Ausgang und
				es ist keine Entfernung zum Ausgang angegeben und
				dieser Nachbar wurde noch nie besucht, muss hier weiter gesuchen!
				"""
				set_color( 'magenta' )
				print( pos, "first visit", unvisitedPos )
				set_color()
				
				print( pos, ">>", unvisitedPos, DistToEscape[pos] )
				temp = findEscape( Field, unvisitedPos, route )
				print( pos, "<<", unvisitedPos, temp )
			
			"""
			Habe einen Nachbarn überprüft.
			
			Wenn eine Entfernung zum Ausgang angegeben wurde, muss für diesen Punkt eine 
			Entfernung gespeichert werden.
			Da auch noch andere Nachbarn eine Distanz bis zum Ziel angeben können, muss
			immer nur die kürzeste Distanz bis zum Ziel gespeichert werden.
			"""
			if temp != None:
				if pos in DistToEscape:
					print( pos, "DistToEscape", DistToEscape[ pos ], "temp", temp )
					minDist = min( DistToEscape[ pos ], temp+1 )
					DistToEscape[ pos ] = minDist
				else:
					DistToEscape[ pos ] = temp + 1
			#####################################################################################
	
	"""
	Nachdem alle Nachbarn überprüft wurden, muss ein Rückgabewert bestimmet werden.
	Wenn diese Instanz die erste Instanz ist mit der die Suche gestartet wurde, dann geben 
	wir die gefundenen Weg zum Ausgang zurück oder eine leere Liste.
	
	Sonst wird überprüft ob irgendein Nachbar eine Entfernung zum Ausgang angegeben hat, 
	dann geben wir unsere Entfernung zum Ausgang zurück.
	Wenn nicht geben wir None zurück
	"""
	if pos != findEscape.first:
		return DistToEscape[ pos ]
	else:
		if isRouteFound:
			FoundLen = str( len( found ) )
			
			sizex, sizey = terminalsize.get_terminal_size()
			BL = "# "
			BR = " #"
			sizex_mid = sizex - len(BL) - len(BR)
			
			
			set_color('green')
			print( "#" * sizex )
			print( BL + "Ausgang gefunden".ljust( sizex_mid ) + BR )
			# print route
			
			zeile = ""
			for element in found:
				# touple in string umwandeln
				el_string = str( element ) + ", "
				el_string = el_string.ljust( 10 )
				# solange zeile nicht voll ist, el anhängen
				if len( zeile ) + len( el_string ) < sizex_mid:
					zeile += el_string
				# sonst zeile ausgeben und zeile weiter füllen
				else:
					# zeile rechts mit whitespace auffüllen
					print( BL + zeile.ljust( sizex_mid ) + BR )
					zeile = el_string
			else:
				# wenn noch nicht alles ausgegeben wurde
				# den rest auch noch ausgeben
				if zeile != "":
					print( BL + zeile.ljust( sizex_mid ) + BR )
			
			print( "#" * sizex )
			#print( found )
			
			#print( "#######################################################" )
			#print( "# Ausgang gefunden                                    #" )
			#print( "#######################################################" )
			
			#drawField()
			SetNewRouteColor()
			drawRoute( found )
		else:
			set_color('red')
			print( "#######################################################" )
			print( "# Kein Ausgang gefunden                               #" )
			print( "#######################################################" )
		
		set_color()
		return found
	

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
	
	findEscapeThread = threading.Thread( target = findEscape, args=(TestField, (1, 1) ) )
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
