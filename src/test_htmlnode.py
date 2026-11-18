import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
	"""Unit Tests for HTMLNode"""
	
	def test_repr_empty(self):
		""" Test HTMLNode.__repr__ for an empty node"""
		node = HTMLNode()
		self.assertEqual("HTMLNode(*,*,*)",repr(node))

	def test_props_to_html(self):
		""" Test HTMLNode.props_to_html for a node props"""
		node = HTMLNode(props={"href":"http://localhost:8888","rel":"something"})
		self.assertEqual(" href=\"http://localhost:8888\" rel=\"something\"",node.props_to_html())

	def test_props_to_html_empty(self):
		""" Test HTMLNode.props_to_html for a node without props"""
		node = HTMLNode()
		self.assertEqual("",node.props_to_html())

	def test_repr_empty_tag(self):
		""" Test HTMLNode.__repr__ for a node without tag"""
		node = HTMLNode(value="val",props={"href":"http://localhost:8888","rel":"something"})
		self.assertEqual("HTMLNode(*,val, href=\"http://localhost:8888\" rel=\"something\")",repr(node))

	def test_repr_empty_value(self):
		""" Test HTMLNode.__repr__ for a node without value"""
		node = HTMLNode(tag="tag",props={"href":"http://localhost:8888","rel":"something"})
		self.assertEqual("HTMLNode(tag,*, href=\"http://localhost:8888\" rel=\"something\")",repr(node))

	def test_repr_empty_props(self):
		""" Test HTMLNode.__repr__ for a node without value"""
		node = HTMLNode(tag="tag",value="value")
		self.assertEqual("HTMLNode(tag,value,*)",repr(node))

	def test_repr_with_children(self):
		""" Test HTMLNode.__repr__ with children"""
		child1 = HTMLNode(tag="c1")
		child3 = HTMLNode(tag="c3")
		child2 = HTMLNode(tag="c2",children=[child3])
		node = HTMLNode(tag="parent",children=[child1,child2])
		self.assertEqual(
			"HTMLNode(parent,*,*)\n" +
			"\tHTMLNode(c1,*,*)\n" +
			"\tHTMLNode(c2,*,*)\n" +
			"\t\tHTMLNode(c3,*,*)",repr(node)
			)



