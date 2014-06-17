#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from Stack import Stack

class Tower( Stack ):
	"""
	"""
	
	def __init__(self, name="None" ):
		super(Tower, self).__init__()
		self.name = name
	
	def removeDisk(self):
		return self.pop()
	
	def pileDisk(self, Disk):
		if not self.isEmpty():
			assert self.peek() > Disk, 'Can not pile Disk, because it is to big'
		self.push( Disk )
	
	def __str__(self):
		return "Tower {0}: {1}".format( self.name, self.Nodes )
	

def printTowers( Tower1, Tower2, Tower3 ):
	Towers = [ Tower1, Tower2, Tower3 ]
	# Sort Towers
	if Towers[0].name != "Left":
		Towers[0], Towers[1] = Towers[1], Towers[0]
	
	if Towers[0].name != "Left":
		Towers[0], Towers[2] = Towers[2], Towers[0]
	
	if Towers[1].name != "Hilf":
		Towers[1], Towers[2] = Towers[2], Towers[1]
	
	print( Towers[0] )
	print( Towers[1] )
	print( Towers[2] )
	print( "" )

def TowerOfHanoi( NumberOfDisks=3 ):
	def move( NumberOfDisks, LeftTower, HilfTower, ZielTower ):
		"""
		Move NumberOfDisks from LeftTower to ZielTower.
		This is done like this.
		Move NumberOfDisks-1 Disks from LeftTower to HilfTower using another Monk.
		Then move lowest Disk to ZielTower.
		After that move NumberOfDisks-1 from HilfTower to ZielTower using another Monk.
		"""
		if NumberOfDisks > 0:
			#print( "Moving", NumberOfDisks, "Disks from", LeftTower.name, "to", ZielTower.name )
			#printTowers( LeftTower, HilfTower, ZielTower )
			move( NumberOfDisks-1, LeftTower, ZielTower, HilfTower )
			
			data = LeftTower.removeDisk()
			ZielTower.pileDisk( data )
			print( "Monk with rank %d moved Disk" % NumberOfDisks, data, "from", LeftTower.name, "to", ZielTower.name )
			printTowers( LeftTower, HilfTower, ZielTower )
			
			#print( "Moving", NumberOfDisks, "from", HilfTower.name, "to", ZielTower.name )
			move( NumberOfDisks-1, HilfTower, LeftTower, ZielTower )
	
	LeftTower = Tower( name="Left" )
	HilfTower = Tower( name="Hilf" )
	ZielTower = Tower( name="Ziel" )
	
	for DiskSize in range( NumberOfDisks, 0, -1 ):
		LeftTower.pileDisk( DiskSize )
	
	print( "Start:" )
	printTowers( LeftTower, HilfTower, ZielTower )
	
	move( NumberOfDisks, LeftTower, HilfTower, ZielTower )
	
	print( "Done" )

if __name__ == "__main__":
	TowerOfHanoi( 10 )
