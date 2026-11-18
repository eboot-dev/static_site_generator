import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
	"""Unit Tests for LeafNode"""
	
	def test_repr_empty(self):
		""" Test LeafNode.__repr__ for an empty node"""
		node = LeafNode(None,"ciao")
		self.assertEqual("LeafNode(*,ciao,*)",repr(node))


	def test_repr_empty_tag(self):
		""" Test LeafNode.__repr__ for a node without tag"""
		node = LeafNode(None,"val",props={"href":"http://localhost:8888","rel":"something"})
		self.assertEqual("LeafNode(*,val, href=\"http://localhost:8888\" rel=\"something\")",repr(node))

	def test_repr_empty_props(self):
		""" Test LeafNode.__repr__ for a node without value"""
		node = LeafNode(tag="tag",value="value")
		self.assertEqual("LeafNode(tag,value,*)",repr(node))

	def test_leaf_to_html(self):
		node = LeafNode("a","Hello, world!",{"href": "https://www.google.com"})
		self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Hello, world!</a>")

	def test_leaf_to_html_empty_props(self):
		node = LeafNode("p","Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")




