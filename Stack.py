#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Stack:
	"""
	"""
	class Node:
		"""
		"""
		def __init__(self, data, next):
			self.data = data
			self.next = next
	
	def __init__(self ): # data=None):
		self.TopNode = None
		self.Size = 0
	
	def isEmpty(self):
		return (self.Size == 0)
	
	@property
	def size(self):
		return self.Size
	
	def push(self, data):
		self.TopNode = self.Node( data, self.TopNode )
		self.Size += 1
	
	def pop(self):
		if self.isEmpty():
			raise Exception('Stack is Empty')
		else:
			returnNode = self.TopNode
			self.TopNode = self.TopNode.next
			self.Size -= 1
			return returnNode.data
	
	def peek(self):
		if self.isEmpty():
			raise Exception('Stack is Empty')
		else:
			return self.TopNode.data

if __name__ == "__main__":
	debug = False
	if debug == True:
		TestData = [ "1. Element", "2. Element", 42, 4.2, "Letztes Element" ]
		
		print( "Testcase for Stack:" )
		
		print( "\nTest push() from Stack class" )
		WorkStack = Stack()
		for el in TestData:
			print( "push to Stack:", el )
			WorkStack.push( el )
		
		print( "\nTest Size of Stack class" )
		print( "Stack size", WorkStack.size )
		
		print( "\nTest peek() from Stack class" )
		data = WorkStack.peek()
		print( "Peeked data from Stack:", data )
		
		print( "\nTest pop() from Stack class" )
		while not WorkStack.isEmpty():
			data = WorkStack.pop()
			print( "Stack data:", data )
		
		print( "\nTest pop() from empty Stack class. Should raise an Exception" )
		try:
			WorkStack.pop()
		except Exception as E:
			print( "Stack raised an Exception" )
		
	
