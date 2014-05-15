#!/usr/bin/python
# -*- coding: UTF-8 -*-

from FloodFill import StripLineEnd, ReadField, PrintField
from FloodFill import emptyMarker, filledMarker, specialMarker, EscapeMarker
'''
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

def PrintField(field):
  for y in range( len(field) ):
    print( "|%s|" % ''.join(field[y]) )
'''
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

def runTests( TestField ):
	print( "Test borders" )
	isFree( TestField,  0,  0 )
	isFree( TestField, -1,  0 )
	isFree( TestField,  0, -1 )
	isFree( TestField,  8,  6 )
	isFree( TestField,  8,  7 )
	isFree( TestField,  9,  6 )

	print( "Test markers" )
	isFree( TestField, 0, 0 )
	isFree( TestField, 1, 0 )
	isFree( TestField, 0, 1 )
	isFree( TestField, 1, 1 )
	
	print( "Test Escape" )
	isEscape( TestField, 0, 0 )
	isEscape( TestField, 1, 1 )
	isEscape( TestField, 1, 2 )
	isEscape( TestField, 7, 2 )


gefundeneRouten = []
#                    , y        , x           , (x0,y0), (x1,y1), ...
def findEscape( Field, rowNumber, columnNumber, route=[] ):
	# format (y,x). >, <, v, ^
	neighbours = ( (0,1), (0,-1), (1,0), (-1,0) )

	print( "--------------------" ) 
	print( route )
	print( "z=%d s=%d %s" % (rowNumber, columnNumber, "suche") )

	if len(route) == 0 :
		route.append( (rowNumber,columnNumber) )
	# test alle Nachbarn, auf Escape
	for n in neighbours:
		Row    = rowNumber    + n[0] # y
		Column = columnNumber + n[1] # x
		pos = (Row, Column)
		# sind wir schon da?
		if isEscape( Field, Row, Column ):
			# Ausgang gefunden route ausgeben, bzw merken
			print( "z=%d s=%d %s" % (Row, Column, "Ausgang gefunden") )
			newRoute = route[:]
			newRoute.append( (Row,Column) )
			print( "**********************************" )
			print( len(newRoute) )
			print( newRoute )
			print( "**********************************" )
			gefundeneRouten.append( [len(newRoute), newRoute] )
			return True

		# ist nachbar frei
		if isFree( Field, Row, Column ):
			print( "z=%d s=%d %s" % (Row, Column, "freier Nachbar") )
			if pos in route:
				print( "NaNaNa hier waren wir doch schon!" )
				#weiter mit nächstem Nachbarn
				continue
			
			newRoute = route[:]
			newRoute.append( (Row,Column) )
			findEscape( Field, Row, Column, newRoute )
			#print( newRoute )
			# waren wir schon hier?
			#pos = (Row, Coumn)
			#if pos in route:
			#	pass
			#	#hier waren wir schon. Markieren, dass es hier nicht weiter geht
			#	#return None
			#else:
			#	pass
			#	#hier waren wir noch nicht
			#	#findEscape aufrufen
	
	print( "hier gehts nicht weiter!" )
	return False

if __name__ == "__main__":
	fileName = "field2.txt"
	TestField = ReadField( fileName )
	#PrintField( TestField )
	
	#runTests( TestField )
	
	findEscape( TestField, 1, 1 )
	
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
	#print( "--------------------" )
	#findEscape( TestField, 7, 1 )
	#print( "--------------------" ) 
	#findEscape( TestField, 7, 3 )
	#print( "--------------------" ) 
	#findEscape( TestField, 3, 4 )
	
