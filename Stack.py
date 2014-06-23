#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Stack:
	"""
	"""
	
	def __init__(self ):
		self.Nodes = []
	
	def isEmpty(self):
		return len(self) == 0
	
	def __len__(self):
		return len(self.Nodes)
	
	def push(self, data):
		self.Nodes.append( data )
	
	def pop(self):
		assert not self.isEmpty(), "Stack is Empty"
		return self.Nodes.pop()
	
	def peek(self):
		assert not self.isEmpty(), "Stack is Empty"
		return self.Nodes[-1]

if __name__ == "__main__":
	TestData = [ "1. Element", "2. Element", 42, 4.2, "Letztes Element" ]
	
	print( "Testcase for Stack:" )
	
	print( "\nTest push() from Stack class" )
	WorkStack = Stack()
	for el in TestData:
		print( "push to Stack:", el )
		WorkStack.push( el )
	
	print( "\nTest Size of Stack class" )
	print( "Stack size", len(WorkStack) )
	
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
