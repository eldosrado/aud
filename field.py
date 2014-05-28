#!/usr/bin/python
# -*- coding: UTF-8 -*-

from FloodFill import StripLineEnd, ReadField, PrintField
from FloodFill import emptyMarker, filledMarker, specialMarker, EscapeMarker
from tkinter import *
import threading
import time
import numpy as np

field = None
app = None
canvas = None
scale = 10
canvas_el = []
input = None
label = None

con = None
runs = 1
#findEscape_runs = 0
#run = False
#Exit = False

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


'''
def printRoute( Field, Route, DeadEnds ):
	pass
'''
def drawField( ):
	pad = 2
	for y in range( len(field) ):
		for x in range( len(field[0]) ):
			x1 = x * scale
			y1 = y * scale
			if field[y][x] == filledMarker:
				canvas.create_rectangle( x1+pad, y1+pad, x1 + scale-pad, y1 + scale-pad, fill="#fb0" )
			if field[y][x] == EscapeMarker:
				canvas.create_rectangle( x1+pad, y1+pad, x1 + scale-pad, y1 + scale-pad, fill="red" )

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

def drawLine( pos1, pos2 ):
	pad = 5
	x1 = pos1[1] * scale
	y1 = pos1[0] * scale
	x2 = pos2[1] * scale
	y2 = pos2[0] * scale
	nr = canvas.create_line( x1+pad, y1+pad, x2+pad, y2+pad, fill="blue", width=3 )
	canvas_el.append( nr )

def drawDot( pos ):
	pad = 2
	x1 = pos[1] * scale
	y1 = pos[0] * scale
	nr = canvas.create_oval( x1+pad, y1+pad, x1 + scale-pad, y1 + scale-pad, fill="blue" )
	canvas_el.append( nr )

def drawRing( pos ):
	pad = 2
	x1 = pos[1] * scale
	y1 = pos[0] * scale
	nr = canvas.create_oval( x1+pad, y1+pad, x1 + scale-pad, y1 + scale-pad, fill="" )
	#canvas_el.append( nr )

def drawRoute( Route ):
	global canvas_el
	# clear previous route
	for el in canvas_el:
		canvas.delete( el )
	
	#draw lines
	for index in range( len(Route)-1 ):
		drawLine( Route[index], Route[index+1] )
	
	#draw dots
	for pos in Route:
		drawDot( pos )

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

def findEscape( Field, rowNumber, columnNumber, route=() ):
	global con
	global runs
	
	if runs < 0:
		return list()
	
	#sync thread
	# wait for runs to be not 0
	con.acquire()
	while runs == 0:
		print( "findEscape is waiting\n" )
		con.wait()
	#print( "findEscape is running" )
	runs -= 1
	con.release()
	
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
	print( route )
	
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
			print( "****************************" )
			
			if not FreierNachbar in route:
				print( FreierNachbar, "frei => hier weitersuchen" )
				nichtBesucht.append( FreierNachbar )
				drawRing( FreierNachbar )
			else:
				#print( FreierNachbar, "dieser Punkt ist schon in der route" )
				TeilRoute = route[:-2]
				#print( "TeilRoute\n", TeilRoute )
				if FreierNachbar in TeilRoute:
					print( FreierNachbar, "hier kann ich optimieren" )
					i = route.index( FreierNachbar )
					print( i, "index" )
					neueRoute = route[:i+1]
					neueRoute.append( pos )
					print( "neueRoute\n", neueRoute )
		
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

'''
def myThreadTest( x=1, y=1, route=() ):
	global runtime
	global con
	
	#while exit not found do bla bla bla
	while not Exit:
		con.acquire()
		while runtime == 0:
			con.wait()
			print( "bla from myThreadTest" )
		
		for i in range( runtime ):
			print( "%s %s %s %s" % (i, x, y, route) )
		
		runtime = 0
		con.release()
'''

if __name__ == "__main__":
	
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
	
	#findEscapeThread = threading.Thread( target = myThreadTest, args=(1,1) )
	findEscapeThread = threading.Thread( target = findEscape, args=(TestField, 1, 1) )
	findEscapeThread.start()
	
	app.mainloop()
	
	print( "kill findEscapeThread" )
	# kill findEscapeThread
	con.acquire()
	#Exit = True
	runs = -1
	con.notify()
	con.release()
	findEscapeThread.join()