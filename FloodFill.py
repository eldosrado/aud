#!/usr/bin/python
# -*- coding: UTF-8 -*-
# AUD Übung 7
# Schreiben Sie eine Flood-Fill-Algorithmus, der ein umrandetes Spielfeld mit
# Zeichen ausfüllt. Das Spielfeld wird als Liste erzeugt.
# Die Liste enthält als Elemente wiederum Zeilen-Listen. Das Spielfeld hat
# z.B. die Größe numberOfColumns=20 und numberOfRows=10 und enthält
# in Zeile 1 und 8 und in Spalte 3 und 15 „x“e als Spielfeldumrandung.
# x = colum = Spalte
# y = row = Zeile

import os

# Verwenden Sie emptyMarker = " "  und filledMarker = "x"
emptyMarker     = " ";
filledMarker    = "x";
specialMarker   = "*"
EscapeMarker    = "E"
numberOfColumns = 40; # x
numberOfRows    = 10; # y

InstanceCounter = 0

# Erzeugen Sie das leer Spielfeld field in der angegebenen Größe
# field = [x][y]

def PrintField(field):
	for y in range( len(field) ):
		print( "|%s|" % ''.join(field[y]) )
		#for x in range( len(field[0]) ):
	print()


def CreateField():
	# feld mit ' 'erstellen
	# numberOfColumns * numberOfRows
	#field = [[emptyMarker] * numberOfColumns ] * numberOfRows

	# Leere Zeile erstellen
	row = [emptyMarker] * numberOfColumns
	# linken und rechten Rand erstellen
	row[ 2] = filledMarker
	row[-3] = filledMarker

	# field erstellen
	# geht nicht! ergibt numberOfRows mal referenz auf row
	# field = [list(row)] * numberOfRows

	# 1. länger und verständlicher 
	#field = []
	#for i in range(numberOfRows):
	#    field.append( list(row) )

	# 2. mit Lambda ausdruck
	field = [ row[:] for i in range(numberOfRows)]

	# oberen und unteren Rand erstellen
	row = [filledMarker] * numberOfColumns
	field[ 1] = list(row)
	field[-2] = list(row)

	return field

def StripLineEnd( string ):
	while string[-1:] in "\r\n":
		string = string[0:-1]
	return string 

def ReadField( FileName ):
	field = []
	file = open( FileName, "r" )
	for line in file:
		#line = line.strip()
		line = StripLineEnd(line)
		lineList = []
		for char in line:
			lineList.append(char)
		field.append(lineList)
	return field 

def FloodFill(field, xpos, ypos):
	global InstanceCounter
	InstanceCounter = InstanceCounter + 1
	print( "Flood-Fill %4d at x=%d y=%d" % (InstanceCounter, xpos, ypos) )

	if field[xpos][ypos] == emptyMarker:
		field[xpos][ypos] = specialMarker
		print( "Fill at x=%d y=%d" % (xpos, ypos) )
		os.system("cls")
		PrintField( field )

	xoff = [ 1, -1]
	yoff = [-1, 1]
	for y in range( len(yoff) ):
		xnew = xpos
		ynew = ypos + yoff[y]
		#print( "xnew=%d ynew=%d" % (xnew, ynew) )
		if field[xnew][ynew] == emptyMarker:
			FloodFill( field, xnew, ynew )
		
	for x in range( len(xoff) ):
		xnew = xpos + yoff[x]
		ynew = ypos
		#print( "xnew=%d ynew=%d" % (xnew, ynew) )
		if field[xnew][ynew] == emptyMarker:
			FloodFill( field, xnew, ynew )
		
		
		#    FloodFill( field, xnew, ynew )
		#print()

	InstanceCounter = InstanceCounter - 1
	pass

if __name__ == "__main__":
	#TestField = CreateField()
	TestField = ReadField("field.txt")
	PrintField( TestField )
	FloodFill( TestField, 5, 5 )
